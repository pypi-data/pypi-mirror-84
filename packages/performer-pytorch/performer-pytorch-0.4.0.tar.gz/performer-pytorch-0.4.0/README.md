<img src="./favor+.png" width="500px"></img>

## Performer - Pytorch

[![PyPI version](https://badge.fury.io/py/performer-pytorch.svg)](https://badge.fury.io/py/performer-pytorch)

An implementation of <a href="https://arxiv.org/abs/2009.14794">Performer</a>, a linear attention-based transformer variant with a **F**ast **A**ttention **V**ia positive **O**rthogonal **R**andom features approach (FAVOR+).

## Install

```bash
$ pip install performer-pytorch
```

## Usage

Performer Language Model

```python
import torch
from performer_pytorch import PerformerLM

model = PerformerLM(
    num_tokens = 20000,
    max_seq_len = 2048,             # max sequence length
    dim = 512,                      # dimension
    depth = 6,                      # layers
    heads = 8,                      # heads
    causal = False,                 # auto-regressive or not
    nb_features = 256,              # number of random features, if not set, will default to (d * log(d)), where d is the dimension of each head
    generalized_attention = False,  # defaults to softmax approximation, but can be set to True for generalized attention
    kernel_fn = nn.ReLU(),          # the kernel function to be used, if generalized attention is turned on, defaults to Relu
    reversible = True,              # reversible layers, from Reformer paper
    ff_chunks = 10,                 # chunk feedforward layer, from Reformer paper
    use_scalenorm = False,          # use scale norm, from 'Transformers without Tears' paper
    use_rezero = False,             # use rezero, from 'Rezero is all you need' paper
    tie_embedding = False           # multiply final embeddings with token weights for logits, like gpt decoder
)

x = torch.randint(0, 20000, (1, 2048))
mask = torch.ones_like(x).bool()

model(x, mask = mask) # (1, 2048, 20000)
```

Plain Performer, if you are working with say images or other modalities

```python
import torch
from performer_pytorch import Performer

model = Performer(
    dim = 512,
    depth = 1,
    heads = 8,
    causal = True
)

x = torch.randn(1, 2048, 512)
model(x) # (1, 2048, 512)
```

Standalone self-attention layer with linear complexity in respect to sequence length, for replacing trained full-attention transformer self-attention layers.

```python
import torch
from performer_pytorch import SelfAttention

attn = SelfAttention(
    dim = 512,
    heads = 8,
    causal = False,
).cuda()

x = torch.randn(1, 1024, 512).cuda()
attn(x) # (1, 1024, 512)
```

## Citations

```bibtex
@misc{choromanski2020rethinking,
    title   = {Rethinking Attention with Performers},
    author  = {Krzysztof Choromanski and Valerii Likhosherstov and David Dohan and Xingyou Song and Andreea Gane and Tamas Sarlos and Peter Hawkins and Jared Davis and Afroz Mohiuddin and Lukasz Kaiser and David Belanger and Lucy Colwell and Adrian Weller},
    year    = {2020},
    eprint  = {2009.14794},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```

```bibtex
@inproceedings{kitaev2020reformer,
    title       = {Reformer: The Efficient Transformer},
    author      = {Nikita Kitaev and Lukasz Kaiser and Anselm Levskaya},
    booktitle   = {International Conference on Learning Representations},
    year        = {2020},
    url         = {https://openreview.net/forum?id=rkgNKkHtvB}
}
```

```bibtex
@inproceedings{katharopoulos_et_al_2020,
    author  = {Katharopoulos, A. and Vyas, A. and Pappas, N. and Fleuret, F.},
    title   = {Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention},
    booktitle = {Proceedings of the International Conference on Machine Learning (ICML)},
    year    = {2020}
}
```

```bibtex
@misc{bachlechner2020rezero,
    title   = {ReZero is All You Need: Fast Convergence at Large Depth},
    author  = {Thomas Bachlechner and Bodhisattwa Prasad Majumder and Huanru Henry Mao and Garrison W. Cottrell and Julian McAuley},
    year    = {2020},
    url     = {https://arxiv.org/abs/2003.04887}
}
```

```bibtex
@article{1910.05895,
    author  = {Toan Q. Nguyen and Julian Salazar},
    title   = {Transformers without Tears: Improving the Normalization of Self-Attention},
    year    = {2019},
    eprint  = {arXiv:1910.05895},
    doi     = {10.5281/zenodo.3525484},
}
```
