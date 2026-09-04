"""
JobGuard Core Optimization - Dynamic Programming & Bellman Equations
Solves discrete 0/1 Knapsack, Longest Common Subsequence, and
Value Iteration / Policy Iteration for Markov Decision Processes (MDP).
"""

from typing import List, Tuple, Dict, Optional


class DynamicProgrammingSolvers:
    """Classic dynamic programming routines for security resource constraints."""

    @staticmethod
    def knapsack_01(values: List[float], weights: List[int], capacity: int) -> Tuple[float, List[int]]:
        """Find max value subset of items fitting within weight capacity."""
        n = len(values)
        dp = [[0.0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            w = weights[i - 1]
            v = values[i - 1]
            for c in range(capacity + 1):
                if w <= c:
                    dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
                else:
                    dp[i][c] = dp[i - 1][c]

        # Backtrack chosen items
        chosen = []
        c = capacity
        for i in range(n, 0, -1):
            if dp[i][c] != dp[i - 1][c]:
                chosen.append(i - 1)
                c -= weights[i - 1]

        chosen.reverse()
        return round(dp[n][capacity], 2), chosen

    @staticmethod
    def longest_common_subsequence(s1: str, s2: str) -> str:
        """Computes exact LCS string for sequence diffing."""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Reconstruct
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if s1[i - 1] == s2[j - 1]:
                lcs.append(s1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return "".join(reversed(lcs))
