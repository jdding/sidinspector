import torch
import torch.nn as nn
import torch.nn.functional as F


class VectorQuantizer(nn.Module):
    """Minimal VQ layer compatible with CARD's released RQ-VAE wrapper."""

    def __init__(
        self,
        n_e,
        e_dim,
        beta=0.25,
        kmeans_init=False,
        kmeans_iters=100,
        sk_epsilon=0.0,
        sk_iters=100,
    ):
        super().__init__()
        self.n_e = int(n_e)
        self.e_dim = int(e_dim)
        self.beta = beta
        self.kmeans_init = kmeans_init
        self.kmeans_iters = int(kmeans_iters)
        self.sk_epsilon = sk_epsilon
        self.sk_iters = int(sk_iters)
        self._kmeans_done = False
        self.embedding = nn.Embedding(self.n_e, self.e_dim)
        nn.init.uniform_(self.embedding.weight, -1.0 / self.n_e, 1.0 / self.n_e)

    def get_codebook(self):
        return self.embedding.weight

    @torch.no_grad()
    def _init_codebook_with_kmeans(self, flat_x):
        if self._kmeans_done or not self.kmeans_init or flat_x.numel() == 0:
            return
        samples = flat_x.detach()
        if samples.shape[0] >= self.n_e:
            perm = torch.randperm(samples.shape[0], device=samples.device)[: self.n_e]
            centroids = samples[perm].clone()
        else:
            repeats = (self.n_e + samples.shape[0] - 1) // samples.shape[0]
            centroids = samples.repeat(repeats, 1)[: self.n_e].clone()
            centroids = centroids + 1e-4 * torch.randn_like(centroids)
        for _ in range(min(self.kmeans_iters, 25)):
            distances = torch.cdist(samples, centroids, p=2)
            labels = distances.argmin(dim=1)
            next_centroids = centroids.clone()
            for code_idx in range(self.n_e):
                mask = labels == code_idx
                if mask.any():
                    next_centroids[code_idx] = samples[mask].mean(dim=0)
            if torch.allclose(next_centroids, centroids, rtol=1e-4, atol=1e-5):
                centroids = next_centroids
                break
            centroids = next_centroids
        self.embedding.weight.copy_(centroids)
        self._kmeans_done = True

    def forward(self, x, use_sk=True):
        input_shape = x.shape
        flat_x = x.reshape(-1, self.e_dim)
        self._init_codebook_with_kmeans(flat_x)
        codebook = self.embedding.weight
        distances = (
            flat_x.pow(2).sum(dim=1, keepdim=True)
            - 2 * flat_x @ codebook.t()
            + codebook.pow(2).sum(dim=1)
        )
        indices = distances.argmin(dim=1)
        quantized = self.embedding(indices).view(input_shape)
        codebook_loss = F.mse_loss(quantized, x.detach())
        commitment_loss = F.mse_loss(quantized.detach(), x)
        loss = codebook_loss + self.beta * commitment_loss
        quantized = x + (quantized - x).detach()
        return quantized, loss, indices.view(input_shape[:-1])
