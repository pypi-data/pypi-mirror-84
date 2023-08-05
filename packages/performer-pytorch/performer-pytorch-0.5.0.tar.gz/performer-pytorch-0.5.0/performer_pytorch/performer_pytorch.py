import math
import torch
import torch.nn.functional as F
from torch import nn
from einops import rearrange
from functools import partial

from performer_pytorch.reversible import ReversibleSequence, SequentialSequence

# helpers

def exists(val):
    return val is not None

def default(val, d):
    return val if exists(val) else d

# kernel functions

# transcribed from jax to pytorch from
# https://github.com/google-research/google-research/blob/master/performer/fast_self_attention/fast_self_attention.py

def softmax_kernel(data, *, projection_matrix, is_query, normalize_data=True, eps=1e-4, device = None):
    if normalize_data:
        data_normalizer = 1.0 / (data.shape[-1] ** 0.25)
    else:
        data_normalizer = 1.0

    ratio = 1.0 / (projection_matrix.shape[0] ** 0.5)

    data_mod_shape = data.shape[:(len(data.shape) - 2)] + projection_matrix.shape
    data_thick_random_matrix = torch.zeros(data_mod_shape, device = device) + projection_matrix

    data_dash = torch.einsum('...id,...jd->...ij', (data_normalizer * data), data_thick_random_matrix)

    diag_data = data ** 2
    diag_data = torch.sum(diag_data, dim=-1)
    diag_data = (diag_data / 2.0) * (data_normalizer ** 2)
    diag_data = diag_data.unsqueeze(dim=-1)

    if is_query:
        data_dash = ratio * (
            torch.exp(data_dash - diag_data -
                    torch.max(data_dash, dim=-1, keepdim=True).values) + eps)
    else:
        data_dash = ratio * (
            torch.exp(data_dash - diag_data - torch.max(data_dash)) + eps)

    return data_dash

def generalized_kernel(data, *, projection_matrix, kernel_fn = nn.ReLU(), kernel_epsilon = 0.001, normalize_data = True, device = None):
    if normalize_data:
        data_normalizer = 1.0 / (data.shape[-1] ** 0.25)
    else:
        data_normalizer = 1.0

    if projection_matrix is None:
        return kernel_fn(data_normalizer * data) + kernel_epsilon

    data_mod_shape = data.shape[0:len(data.shape) - 2] + projection_matrix.shape
    data_thick_random_matrix = torch.zeros(data_mod_shape, device = device) + projection_matrix

    data_dash = torch.einsum('...id,...jd->...ij', (data_normalizer * data), data_thick_random_matrix)

    data_prime = kernel_fn(data_dash) + kernel_epsilon
    return data_prime

def orthogonal_matrix_chunk(cols, qr_uniform_q = False, device = None):
    unstructured_block = torch.randn((cols, cols), device = device)
    q, r = torch.qr(unstructured_block.cpu(), some = True)
    q, r = map(lambda t: t.to(device), (q, r))

    # proposed by @Parskatt
    # to make sure Q is uniform https://arxiv.org/pdf/math-ph/0609050.pdf
    if qr_uniform_q:
        d = torch.diag(r, 0)
        q *= d.sign()
    return q.t()

def gaussian_orthogonal_random_matrix(nb_rows, nb_columns, scaling = 0, qr_uniform_q = False, device = None):
    nb_full_blocks = int(nb_rows / nb_columns)

    block_list = []

    for _ in range(nb_full_blocks):
        q = orthogonal_matrix_chunk(nb_columns, qr_uniform_q = qr_uniform_q, device = device)
        block_list.append(q)

    remaining_rows = nb_rows - nb_full_blocks * nb_columns
    if remaining_rows > 0:
        q = orthogonal_matrix_chunk(nb_columns, qr_uniform_q = qr_uniform_q, device = device)
        block_list.append(q[:remaining_rows])

    final_matrix = torch.cat(block_list)

    if scaling == 0:
        multiplier = torch.randn((nb_rows, nb_columns), device = device).norm(dim = 1)
    elif scaling == 1:
        multiplier = math.sqrt((float(nb_columns))) * torch.ones((nb_rows,), device = device)
    else:
        raise ValueError(f'Invalid scaling {scaling}')

    return torch.diag(multiplier) @ final_matrix

# linear attention classes with softmax kernel

# non-causal linear attention
def linear_attention(q, k, v):
    D_inv = 1. / torch.einsum('...nd,...d->...n', q, k.sum(dim = -2))
    context = torch.einsum('...nd,...ne->...de', k, v)
    out = torch.einsum('...de,...nd,...n->...ne', context, q, D_inv)
    return out

# efficient causal linear attention, created by EPFL
def causal_linear_attention(q, k, v):
    from fast_transformers.causal_product import CausalDotProduct
    return CausalDotProduct.apply(q, k, v)

# inefficient causal linear attention, without cuda code, for reader's reference
# not being used
def causal_linear_attention_noncuda(q, k, v):
    k_cumsum = k.cumsum(dim=-2)
    context = torch.einsum('...nd,...ne->...nde', k, v)
    context = context.cumsum(dim=-3)
    context /= k_cumsum.unsqueeze(dim=-1)
    out = torch.einsum('...nde,...nd->...ne', context, q)
    return out

class FastAttention(nn.Module):
    def __init__(self, dim_heads, nb_features = None, redraw_projection = True, ortho_scaling = 0, causal = False, generalized_attention = False, kernel_fn = nn.ReLU(), qr_uniform_q = False):
        super().__init__()
        nb_features = default(nb_features, int(dim_heads * math.log(dim_heads)))

        self.dim_heads = dim_heads
        self.nb_features = nb_features
        self.ortho_scaling = ortho_scaling
        self.redraw_projection = redraw_projection

        self.create_projection = partial(gaussian_orthogonal_random_matrix, nb_rows = self.nb_features, nb_columns = dim_heads, scaling = ortho_scaling, qr_uniform_q = qr_uniform_q)

        self.generalized_attention = generalized_attention
        self.kernel_fn = kernel_fn

        if not redraw_projection:
            projection_matrix = self.create_projection()
            self.register_buffer('projection_matrix', projection_matrix)

        self.causal = causal
        if causal:
            try:
                import fast_transformers.causal_product.causal_product_cuda
                self.causal_linear_fn = causal_linear_attention
            except ImportError:
                print('unable to import cuda code for auto-regressive Performer. will default to the memory inefficient non-cuda version')
                self.causal_linear_fn = causal_linear_attention_noncuda

    def forward(self, q, k, v):
        device = q.device

        if self.redraw_projection:
            projection_matrix = self.create_projection(device = device)
        else:
            projection_matrix = self.projection_matrix

        if self.generalized_attention:
            create_kernel = partial(generalized_kernel, kernel_fn = self.kernel_fn, projection_matrix = projection_matrix, device = device)
            q, k = map(create_kernel, (q, k))
        else:
            create_kernel = partial(softmax_kernel, projection_matrix = projection_matrix, device = device)
            q = create_kernel(q, is_query = True)
            k = create_kernel(k, is_query = False)

        attn_fn = linear_attention if not self.causal else self.causal_linear_fn
        out = attn_fn(q, k, v)
        return out

# classes

class ReZero(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.g = nn.Parameter(torch.zeros(1))
        self.fn = fn

    def forward(self, x, **kwargs):
        return self.fn(x, **kwargs) * self.g

class PreScaleNorm(nn.Module):
    def __init__(self, dim, fn, eps=1e-5):
        super().__init__()
        self.fn = fn
        self.g = nn.Parameter(torch.ones(1))
        self.eps = eps

    def forward(self, x, **kwargs):
        n = torch.norm(x, dim=-1, keepdim=True).clamp(min=self.eps)
        x = x / n * self.g
        return self.fn(x, **kwargs)

class PreLayerNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.fn = fn
    def forward(self, x, **kwargs):
        return self.fn(self.norm(x), **kwargs)

class Chunk(nn.Module):
    def __init__(self, chunks, fn, along_dim = -1):
        super().__init__()
        self.dim = along_dim
        self.chunks = chunks
        self.fn = fn

    def forward(self, x, **kwargs):
        if self.chunks == 1:
            return self.fn(x, **kwargs)
        chunks = x.chunk(self.chunks, dim = self.dim)
        return torch.cat([self.fn(c, **kwargs) for c in chunks], dim = self.dim)

class FeedForward(nn.Module):
    def __init__(self, dim, mult = 4, dropout = 0., activation = None, glu = False):
        super().__init__()
        activation = default(activation, nn.GELU)

        self.glu = glu
        self.w1 = nn.Linear(dim, dim * mult * (2 if glu else 1))
        self.act = activation()
        self.dropout = nn.Dropout(dropout)
        self.w2 = nn.Linear(dim * mult, dim)

    def forward(self, x, **kwargs):
        if not self.glu:
            x = self.w1(x)
            x = self.act(x)
        else:
            x, v = self.w1(x).chunk(2, dim=-1)
            x = self.act(x) * v

        x = self.dropout(x)
        x = self.w2(x)
        return x

class SelfAttention(nn.Module):
    def __init__(self, dim, causal = False, heads = 8, nb_features = None, redraw_projection = True, generalized_attention = False, kernel_fn = nn.ReLU(), qr_uniform_q = False, dropout = 0.):
        super().__init__()
        assert dim % heads == 0, 'dimension must be divisible by number of heads'
        self.fast_attention = FastAttention(dim // heads, nb_features, redraw_projection, causal = causal, generalized_attention = generalized_attention, kernel_fn = kernel_fn, qr_uniform_q = qr_uniform_q)

        self.heads = heads
        self.to_qkv = nn.Linear(dim, dim * 3, bias = False)
        self.to_out = nn.Linear(dim, dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask = None):
        b, n, _, h = *x.shape, self.heads
        qkv = self.to_qkv(x).chunk(3, dim = -1)

        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h = h), qkv)

        if exists(mask):
            mask = mask[:, None, :, None]
            k.masked_fill_(~mask, 0)

        out = self.fast_attention(q, k, v)

        out = rearrange(out, 'b h n d -> b n (h d)')
        out =  self.to_out(out)
        return self.dropout(out)

class Performer(nn.Module):
    def __init__(self, dim, depth, heads, causal = False, ff_mult = 4, nb_features = None, reversible = False, ff_chunks = 1, generalized_attention = False, kernel_fn = nn.ReLU(), qr_uniform_q = False, use_scalenorm = False, use_rezero = False, ff_glu = False, ff_dropout = 0., attn_dropout = 0.):
        super().__init__()
        layers = nn.ModuleList([])

        if use_scalenorm:
            wrapper_fn = partial(PreScaleNorm, dim)
        elif use_rezero:
            wrapper_fn = ReZero
        else:
            wrapper_fn = partial(PreLayerNorm, dim)

        for _ in range(depth):
            layers.append(nn.ModuleList([
                wrapper_fn(SelfAttention(dim, causal = causal, heads = heads, nb_features = nb_features, generalized_attention = generalized_attention, kernel_fn = kernel_fn, qr_uniform_q = qr_uniform_q, dropout = attn_dropout)),
                wrapper_fn(Chunk(ff_chunks, FeedForward(dim, mult = ff_mult, dropout = ff_dropout, glu = ff_glu), along_dim = 1))
            ]))

        execute_type = ReversibleSequence if reversible else SequentialSequence
        route_attn = ((True, False),) * depth
        attn_route_map = {'mask': route_attn}
        self.net = execute_type(layers, args_route = {**attn_route_map})

    def forward(self, x, **kwargs):
        return self.net(x, **kwargs)

class PerformerLM(nn.Module):
    def __init__(self, *, num_tokens, max_seq_len, dim, depth, heads, causal = False, ff_mult = 4, nb_features = None, reversible = False, ff_chunks = 1, ff_glu = False, emb_dropout = 0., ff_dropout = 0., attn_dropout = 0., generalized_attention = False, kernel_fn = nn.ReLU(), qr_uniform_q = False, use_scalenorm = False, use_rezero = False, tie_embedding = False):
        super().__init__()
        self.max_seq_len = max_seq_len
        self.token_emb = nn.Embedding(num_tokens, dim)
        self.pos_emb = nn.Embedding(max_seq_len, dim)
        self.dropout = nn.Dropout(emb_dropout)

        nn.init.normal_(self.token_emb.weight, std = 0.02)
        nn.init.normal_(self.pos_emb.weight, std = 0.02)

        self.performer = Performer(dim, depth, heads, causal, ff_mult, nb_features, reversible, ff_chunks, generalized_attention, kernel_fn, qr_uniform_q, use_scalenorm, use_rezero, ff_glu, ff_dropout, attn_dropout)
        self.norm = nn.LayerNorm(dim)

        if tie_embedding:
            self.to_logits = lambda t: t @ self.token_emb.weight.t()
        else:
            self.to_logits = nn.Linear(dim, num_tokens)

    def forward(self, x, **kwargs):
        b, n, device = *x.shape, x.device
        # token and positoinal embeddings
        x = self.token_emb(x)
        x += self.pos_emb(torch.arange(n, device = device))
        x = self.dropout(x)

        # performer layers
        x = self.performer(x, **kwargs)

        # norm and to logits
        x = self.norm(x)
        return self.to_logits(x)
