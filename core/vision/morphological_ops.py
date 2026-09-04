"""
JobGuard Core Vision - Mathematical Morphology (Dilation, Erosion, Opening, Closing)
Binary and grayscale structuring element operations for character stroke repair.
"""

from typing import List, Tuple


class MorphologicalOperations:
    """Binary mathematical morphology operations."""

    @staticmethod
    def erode(binary_image: List[List[int]], kernel_size: int = 3) -> List[List[int]]:
        h = len(binary_image)
        w = len(binary_image[0]) if h > 0 else 0
        pad = kernel_size // 2
        out = [[0] * w for _ in range(h)]

        for y in range(h):
            for x in range(w):
                all_fit = True
                for ky in range(-pad, pad + 1):
                    for kx in range(-pad, pad + 1):
                        iy = min(max(0, y + ky), h - 1)
                        ix = min(max(0, x + kx), w - 1)
                        if binary_image[iy][ix] == 0:
                            all_fit = False
                            break
                    if not all_fit:
                        break
                out[y][x] = 1 if all_fit else 0

        return out

    @staticmethod
    def dilate(binary_image: List[List[int]], kernel_size: int = 3) -> List[List[int]]:
        h = len(binary_image)
        w = len(binary_image[0]) if h > 0 else 0
        pad = kernel_size // 2
        out = [[0] * w for _ in range(h)]

        for y in range(h):
            for x in range(w):
                any_hit = False
                for ky in range(-pad, pad + 1):
                    for kx in range(-pad, pad + 1):
                        iy = min(max(0, y + ky), h - 1)
                        ix = min(max(0, x + kx), w - 1)
                        if binary_image[iy][ix] == 1:
                            any_hit = True
                            break
                    if any_hit:
                        break
                out[y][x] = 1 if any_hit else 0

        return out
