"""
JobGuard Backend Service - Recruiter Domain Clustering & Syndicate Intelligence
Identifies syndicated scam rings across shared WHOIS registrars, name server clusters,
common IP subnets, and cloned landing page templates.
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from dataclasses import dataclass, field
import collections
import hashlib


@dataclass
class DomainNode:
    domain: str
    registrar: str
    nameservers: List[str]
    ip_subnet: str
    target_company_impersonated: str
    registration_date: str
    first_seen_timestamp: float
    threat_category: str


@dataclass
class SyndicateCluster:
    cluster_id: str
    primary_threat_actor: str
    associated_domains: List[str]
    shared_infrastructure_traits: List[str]
    targeted_companies: List[str]
    estimated_active_campaigns: int
    cluster_risk_rating: float  # 0 to 100


class RecruiterDomainClusterService:
    """Discovers and clusters coordinated cybercrime campaigns targeting corporate brands."""

    def __init__(self):
        self.domains: Dict[str, DomainNode] = {}
        self.clusters: Dict[str, SyndicateCluster] = {}
        self._seed_known_syndicates()

    def _seed_known_syndicates(self) -> None:
        """Populate initial baseline of known threat syndicate domain clusters."""

        # Syndicate Alpha: Tech Impersonation Ring
        domains_alpha = [
            DomainNode("google-careers-desk.net", "NameCheap Inc", ["ns1.offshore-dns.com", "ns2.offshore-dns.com"], "185.156.72.0/24", "Google", "2026-01-15", 1768435200.0, "FAKE_ATS"),
            DomainNode("microsoft-hr-hiring.com", "NameCheap Inc", ["ns1.offshore-dns.com", "ns2.offshore-dns.com"], "185.156.72.0/24", "Microsoft", "2026-01-18", 1768694400.0, "FAKE_ATS"),
            DomainNode("amazon-onboarding-portal.org", "NameCheap Inc", ["ns1.offshore-dns.com", "ns2.offshore-dns.com"], "185.156.72.0/24", "Amazon", "2026-02-01", 1769904000.0, "FAKE_ATS")
        ]
        for d in domains_alpha:
            self.domains[d.domain] = d

        # Syndicate Beta: Crypto Task Rating Scheme
        domains_beta = [
            DomainNode("global-task-opt.vip", "Tucows Domains", ["ns1.cloudflare.com", "ns2.cloudflare.com"], "104.244.72.0/24", "Generic Brand", "2026-02-10", 1770681600.0, "CRYPTO_TASK"),
            DomainNode("smart-rating-vip.club", "Tucows Domains", ["ns1.cloudflare.com", "ns2.cloudflare.com"], "104.244.72.0/24", "Generic Brand", "2026-02-14", 1771027200.0, "CRYPTO_TASK")
        ]
        for d in domains_beta:
            self.domains[d.domain] = d

    def cluster_infrastructure(self) -> List[SyndicateCluster]:
        """Clusters active domains based on shared nameservers, registrars, and subnets."""
        # Group by nameservers + subnet
        groups = collections.defaultdict(list)
        for domain, node in self.domains.items():
            key = (node.registrar, tuple(sorted(node.nameservers)), node.ip_subnet)
            groups[key].append(node)

        results: List[SyndicateCluster] = []
        for idx, (key, domain_nodes) in enumerate(groups.items()):
            registrar, ns, subnet = key
            dom_list = [d.domain for d in domain_nodes]
            targets = list(set(d.target_company_impersonated for d in domain_nodes))
            traits = [
                f"Shared Registrar: {registrar}",
                f"Identical Nameservers: {', '.join(ns)}",
                f"Co-located Subnet: {subnet}"
            ]
            cluster_id = f"SYN-CLUSTER-{hashlib.md5(str(key).encode()).hexdigest()[:8].upper()}"

            cluster = SyndicateCluster(
                cluster_id=cluster_id,
                primary_threat_actor=f"Syndicate-{chr(65 + idx)}",
                associated_domains=dom_list,
                shared_infrastructure_traits=traits,
                targeted_companies=targets,
                estimated_active_campaigns=len(dom_list),
                cluster_risk_rating=92.0 if len(dom_list) > 1 else 65.0
            )
            results.append(cluster)
            self.clusters[cluster_id] = cluster

        return results

    def add_domain_telemetry(self, node: DomainNode) -> None:
        """Ingests new domain telemetry into clustering pipeline."""
        self.domains[node.domain] = node
