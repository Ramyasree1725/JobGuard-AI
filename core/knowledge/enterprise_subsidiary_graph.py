"""
JobGuard Core Knowledge - Corporate Parent-Subsidiary Graph & Ownership Hierarchy
Maintains directed ownership trees of multinational holding structures (SEC Exhibit 21),
subsidiaries, operating brands, and joint ventures for authentic corporate pedigree verification.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class CorporateEntityNode:
    entity_id: str
    legal_name: str
    jurisdiction_country: str
    ownership_percentage: float = 100.0
    parent_id: Optional[str] = None
    subsidiary_ids: List[str] = field(default_factory=list)
    primary_domain: str = ""
    operating_status: str = "ACTIVE"


class EnterpriseSubsidiaryGraph:
    """Directed Acyclic Graph (DAG) representing corporate ownership trees."""

    def __init__(self):
        self.nodes: Dict[str, CorporateEntityNode] = {}
        self._brand_to_parent: Dict[str, str] = {}
        self._populate_ownership_trees()

    def add_entity(self, entity: CorporateEntityNode) -> None:
        self.nodes[entity.entity_id] = entity
        self._brand_to_parent[entity.legal_name.lower()] = entity.entity_id
        if entity.parent_id and entity.parent_id in self.nodes:
            self.nodes[entity.parent_id].subsidiary_ids.append(entity.entity_id)

    def _populate_ownership_trees(self) -> None:
        """Populate global corporate parent-subsidiary structures."""
        # Alphabet Tree
        self.add_entity(CorporateEntityNode("CORP-ALPHABET", "Alphabet Inc.", "US", primary_domain="abc.xyz"))
        self.add_entity(CorporateEntityNode("SUB-GOOGLE", "Google LLC", "US", parent_id="CORP-ALPHABET", primary_domain="google.com"))
        self.add_entity(CorporateEntityNode("SUB-DEEPMIND", "DeepMind Technologies Limited", "GB", parent_id="CORP-ALPHABET", primary_domain="deepmind.google"))
        self.add_entity(CorporateEntityNode("SUB-WAYMO", "Waymo LLC", "US", parent_id="CORP-ALPHABET", primary_domain="waymo.com"))
        self.add_entity(CorporateEntityNode("SUB-VERILY", "Verily Life Sciences LLC", "US", parent_id="CORP-ALPHABET", primary_domain="verily.com"))

        # Amazon Tree
        self.add_entity(CorporateEntityNode("CORP-AMAZON", "Amazon.com, Inc.", "US", primary_domain="amazon.com"))
        self.add_entity(CorporateEntityNode("SUB-AWS", "Amazon Web Services, Inc.", "US", parent_id="CORP-AMAZON", primary_domain="aws.amazon.com"))
        self.add_entity(CorporateEntityNode("SUB-AUDIBLE", "Audible, Inc.", "US", parent_id="CORP-AMAZON", primary_domain="audible.com"))
        self.add_entity(CorporateEntityNode("SUB-TWITCH", "Twitch Interactive, Inc.", "US", parent_id="CORP-AMAZON", primary_domain="twitch.tv"))
        self.add_entity(CorporateEntityNode("SUB-ZOOX", "Zoox, Inc.", "US", parent_id="CORP-AMAZON", primary_domain="zoox.com"))

        # Microsoft Tree
        self.add_entity(CorporateEntityNode("CORP-MICROSOFT", "Microsoft Corporation", "US", primary_domain="microsoft.com"))
        self.add_entity(CorporateEntityNode("SUB-LINKEDIN", "LinkedIn Corporation", "US", parent_id="CORP-MICROSOFT", primary_domain="linkedin.com"))
        self.add_entity(CorporateEntityNode("SUB-GITHUB", "GitHub, Inc.", "US", parent_id="CORP-MICROSOFT", primary_domain="github.com"))
        self.add_entity(CorporateEntityNode("SUB-NUANCE", "Nuance Communications, Inc.", "US", parent_id="CORP-MICROSOFT", primary_domain="nuance.com"))

        # Meta Tree
        self.add_entity(CorporateEntityNode("CORP-META", "Meta Platforms, Inc.", "US", primary_domain="meta.com"))
        self.add_entity(CorporateEntityNode("SUB-INSTAGRAM", "Instagram, LLC", "US", parent_id="CORP-META", primary_domain="instagram.com"))
        self.add_entity(CorporateEntityNode("SUB-WHATSAPP", "WhatsApp LLC", "US", parent_id="CORP-META", primary_domain="whatsapp.com"))

        # Tata Group Tree
        self.add_entity(CorporateEntityNode("CORP-TATA-SONS", "Tata Sons Private Limited", "IN", primary_domain="tata.com"))
        self.add_entity(CorporateEntityNode("SUB-TCS", "Tata Consultancy Services Limited", "IN", parent_id="CORP-TATA-SONS", primary_domain="tcs.com"))
        self.add_entity(CorporateEntityNode("SUB-TATA-MOTORS", "Tata Motors Limited", "IN", parent_id="CORP-TATA-SONS", primary_domain="tatamotors.com"))
        self.add_entity(CorporateEntityNode("SUB-TATA-ELXSI", "Tata Elxsi Limited", "IN", parent_id="CORP-TATA-SONS", primary_domain="tataelxsi.com"))

    def get_ultimate_parent(self, entity_id: str) -> Optional[CorporateEntityNode]:
        """Traverse upwards to find ultimate controlling corporate parent."""
        if entity_id not in self.nodes:
            return None

        curr = self.nodes[entity_id]
        visited = set()

        while curr.parent_id and curr.parent_id in self.nodes:
            if curr.entity_id in visited:
                break
            visited.add(curr.entity_id)
            curr = self.nodes[curr.parent_id]

        return curr

    def get_all_subsidiaries(self, parent_id: str) -> List[CorporateEntityNode]:
        """BFS traversal to retrieve all direct and indirect subsidiary entities."""
        if parent_id not in self.nodes:
            return []

        subsidiaries = []
        queue = list(self.nodes[parent_id].subsidiary_ids)
        visited = set(queue)

        while queue:
            sub_id = queue.pop(0)
            if sub_id in self.nodes:
                sub_node = self.nodes[sub_id]
                subsidiaries.append(sub_node)
                for child_id in sub_node.subsidiary_ids:
                    if child_id not in visited:
                        visited.add(child_id)
                        queue.append(child_id)

        return subsidiaries
