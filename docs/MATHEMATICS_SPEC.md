# Aetheris Mathematical Foundations & Algorithmic Formulations

## 1. Kinematics & Jacobians
For a manipulator with $N$ joints, the forward transformation matrix from base to end-effector is:
$$T_0^N(q) = \prod_{i=1}^N A_i(q_i)$$
Where Denavit-Hartenberg link transformation $A_i$ is:
$$A_i = \text{Rot}_z(\theta_i) \cdot \text{Trans}_z(d_i) \cdot \text{Trans}_x(a_i) \cdot \text{Rot}_x(\alpha_i)$$

The geometric Jacobian $J(q) \in \mathbb{R}^{6 \times N}$ maps joint velocities to Cartesian velocities:
$$v_e = J_v(q) \dot{q}, \quad \omega_e = J_\omega(q) \dot{q}$$
Where for revolute joints:
$$J_{v, i} = z_{i-1} \times (p_e - p_{i-1}), \quad J_{\omega, i} = z_{i-1}$$

Damped Least-Squares (DLS) Inverse Kinematics resolves singular configurations via:
$$\Delta q = J^T (J J^T + \lambda^2 I)^{-1} e + (I - J^\dagger J) \nabla H(q)$$

## 2. Multi-Objective NSGA-II Pareto Optimization
A solution $x_1$ Pareto-dominates $x_2$ ($x_1 \prec x_2$) if and only if:
$$\forall i \in \{1, \dots, M\}, \quad f_i(x_1) \le f_i(x_2) \quad \land \quad \exists j \in \{1, \dots, M\}, \quad f_j(x_1) < f_j(x_2)$$

Crowding distance metric $d_i$ preserves frontier spread:
$$d_i = \sum_{m=1}^M \frac{f_m(i+1) - f_m(i-1)}{f_m^{\max} - f_m^{\min}}$$

## 3. Gaussian Process Surrogate Regression
Given observations $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$, posterior distribution at test point $x^*$ is Gaussian $\mathcal{N}(\mu(x^*), \sigma^2(x^*))$:
$$\mu(x^*) = k(x^*, X) [K(X, X) + \sigma_n^2 I]^{-1} y$$
$$\sigma^2(x^*) = k(x^*, x^*) - k(x^*, X) [K(X, X) + \sigma_n^2 I]^{-1} k(X, x^*)$$

With Matern 5/2 covariance kernel:
$$k(r) = \sigma_f^2 \left(1 + \frac{\sqrt{5}r}{l} + \frac{5r^2}{3l^2}\right) \exp\left(-\frac{\sqrt{5}r}{l}\right)$$

## 4. Multi-Head Scaled Dot-Product Attention
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}} + M\right) V$$
Where causal mask $M_{ij} = -\infty$ for $j > i$, and $0$ otherwise.
