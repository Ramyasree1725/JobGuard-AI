"""
Aetheris Computer Vision & Spatial: 3D Scene Graph & Semantic Hierarchy
Proprietary Core Algorithm Library - Advanced Research Systems
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
from core.math.vectors import Vector3D
from core.math.matrices import Matrix4x4
from core.math.geometry import AABB3D


class SceneNode:
    """Hierarchical 3D Scene Node with local transform, world transform propagation, and semantic tags."""
    def __init__(self, name: str, local_transform: Optional[Matrix4x4] = None, semantic_label: str = "object") -> None:
        self.name = name
        self.local_transform = local_transform if local_transform is not None else Matrix4x4.identity()
        self.world_transform = Matrix4x4.identity()
        self.semantic_label = semantic_label
        self.children: List[SceneNode] = []
        self.parent: Optional[SceneNode] = None
        self.bounding_box: Optional[AABB3D] = None

    def add_child(self, child: SceneNode) -> None:
        child.parent = self
        self.children.append(child)

    def update_world_transforms(self, parent_world: Optional[Matrix4x4] = None) -> None:
        if parent_world is None:
            self.world_transform = self.local_transform
        else:
            self.world_transform = parent_world * self.local_transform

        for child in self.children:
            child.update_world_transforms(self.world_transform)

    def get_world_position(self) -> Vector3D:
        return self.world_transform.get_translation()

    def find_by_name(self, name: str) -> Optional[SceneNode]:
        if self.name == name:
            return self
        for child in self.children:
            res = child.find_by_name(name)
            if res is not None:
                return res
        return None

    def collect_nodes_with_label(self, label: str, results: List[SceneNode]) -> None:
        if self.semantic_label == label:
            results.append(self)
        for child in self.children:
            child.collect_nodes_with_label(label, results)


class SceneGraph3D:
    """Root container managing the entire virtual environment scene graph hierarchy."""
    def __init__(self, root_name: str = "world_root") -> None:
        self.root = SceneNode(root_name, semantic_label="world")

    def update(self) -> None:
        self.root.update_world_transforms()

    def query_semantic(self, label: str) -> List[SceneNode]:
        results: List[SceneNode] = []
        self.root.collect_nodes_with_label(label, results)
        return results
