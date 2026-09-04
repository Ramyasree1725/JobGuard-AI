"""
JobGuard Core Recommendation - Neural Collaborative Filtering (NCF / NeuMF)
Combines generalized matrix factorization (GMF) and multi-layer perceptron (MLP) branches
for non-linear candidate-job suitability and credibility prediction.
"""

from typing import List, Tuple, Dict, Optional
from core.ml_inference.tensor_engine import Tensor
from core.ml_inference.neural_layers import DenseLayer


class NeuMFModel:
    """Neural Matrix Factorization architecture."""

    def __init__(self, num_users: int = 100, num_items: int = 100, latent_dim_gmf: int = 8, latent_dim_mlp: int = 16):
        self.latent_dim_gmf = latent_dim_gmf
        self.latent_dim_mlp = latent_dim_mlp

        # MLP branch layers
        self.mlp_dense1 = DenseLayer(latent_dim_mlp * 2, 32, activation="relu")
        self.mlp_dense2 = DenseLayer(32, 16, activation="relu")

        # Fusion output layer
        self.final_dense = DenseLayer(latent_dim_gmf + 16, 1, activation="sigmoid")

    def forward(self, gmf_user: Tensor, gmf_item: Tensor, mlp_user: Tensor, mlp_item: Tensor) -> Tensor:
        """Forward pass combining GMF element-wise product and MLP concatenated branch."""
        # GMF branch: element-wise product
        gmf_out = gmf_user.mul(gmf_item)

        # MLP branch: concatenation
        mlp_concat_data = mlp_user.data + mlp_item.data
        mlp_concat = Tensor(mlp_concat_data, shape=(1, self.latent_dim_mlp * 2))
        
        mlp_h1 = self.mlp_dense1.forward(mlp_concat)
        mlp_h2 = self.mlp_dense2.forward(mlp_h1)

        # Concatenate GMF + MLP outputs
        fusion_data = gmf_out.data + mlp_h2.data
        fusion_tensor = Tensor(fusion_data, shape=(1, self.latent_dim_gmf + 16))

        return self.final_dense.forward(fusion_tensor)
