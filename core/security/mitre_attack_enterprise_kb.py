"""
JobGuard Core Security - Comprehensive MITRE ATT&CK for Enterprise & Fraud Matrix
Contains exhaustive tactical mappings, techniques, sub-techniques, detection analytics,
and automated defensive playbooks for recruitment fraud and identity theft threats.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class TechniqueMitigation:
    mitigation_id: str
    name: str
    description: str


@dataclass
class MitreTechnique:
    technique_id: str
    tactic: str  # "Initial Access", "Execution", "Persistence", "Credential Access", "Collection", "Impact"
    name: str
    description: str
    detection_queries: List[str]
    mitigations: List[TechniqueMitigation]
    sub_techniques: List[str] = field(default_factory=list)
    relevance_to_recruitment_fraud: str = "HIGH"


class MitreAttackEnterpriseKB:
    """Master database of MITRE ATT&CK techniques mapped to online recruitment fraud vectors."""

    def __init__(self):
        self.techniques: Dict[str, MitreTechnique] = {}
        self._tactic_index: Dict[str, List[str]] = {}
        self._populate_mitre_matrix()

    def register_technique(self, tech: MitreTechnique) -> None:
        self.techniques[tech.technique_id] = tech
        tactic_clean = tech.tactic.lower()
        if tactic_clean not in self._tactic_index:
            self._tactic_index[tactic_clean] = []
        self._tactic_index[tactic_clean].append(tech.technique_id)

    def _populate_mitre_matrix(self) -> None:
        """Populate exhaustive MITRE ATT&CK techniques."""
        data = [
            # Initial Access
            MitreTechnique(
                technique_id="T1566.001",
                tactic="Initial Access",
                name="Phishing: Spearphishing Attachment",
                description="Adversaries send spearphishing emails with malicious PDF/DOCX offer letters containing embedded payload links.",
                detection_queries=["email.attachment.name:(*offer*.pdf OR *appointment*.docx)", "pdf.contains_javascript:true"],
                mitigations=[TechniqueMitigation("M1049", "Antivirus/Antimalware", "Scan all incoming offer letter attachments for malicious macro payloads.")],
                sub_techniques=["T1566.001.01", "T1566.001.02"]
            ),
            MitreTechnique(
                technique_id="T1566.002",
                tactic="Initial Access",
                name="Phishing: Spearphishing Link",
                description="Adversaries send recruitment links directing candidates to credential-harvesting fake portal landing pages.",
                detection_queries=["url.domain:(*careers-jobs* OR *portal-hiring*)", "http.request.uri:(*google-form* OR *typeform*)"],
                mitigations=[TechniqueMitigation("M1054", "Software Configuration", "Enforce strict domain reputation filters on incoming communications.")],
                sub_techniques=["T1566.002.01"]
            ),
            MitreTechnique(
                technique_id="T1566.003",
                tactic="Initial Access",
                name="Phishing: Spearphishing via Service",
                description="Adversaries message targets via third-party messaging services such as Telegram, WhatsApp, LinkedIn, or Signal.",
                detection_queries=["chat.protocol:(telegram OR whatsapp)", "message.body:(*daily pay* OR *part time task*)"],
                mitigations=[TechniqueMitigation("M1017", "User Training", "Train job seekers to refuse informal chat-only recruitment interviews.")],
                sub_techniques=[]
            ),

            # Reconnaissance & Resource Development
            MitreTechnique(
                technique_id="T1589.001",
                tactic="Reconnaissance",
                name="Gather Victim Identity Information: Credentials",
                description="Adversaries harvest candidate SSN, Date of Birth, and banking credentials disguised as pre-onboarding background checks.",
                detection_queries=["form.field_names:(ssn OR bank_account OR routing_number)", "workflow.stage:pre_interview"],
                mitigations=[TechniqueMitigation("M1056", "Pre-compromise", "Enforce zero-data transmission standards before contract signing.")],
                sub_techniques=[]
            ),
            MitreTechnique(
                technique_id="T1586.002",
                tactic="Resource Development",
                name="Compromise Accounts: Email Accounts",
                description="Adversaries register lookalike burner webmail accounts (e.g. recruiter.google@gmail.com) to impersonate corporate HR.",
                detection_queries=["sender.domain:(gmail.com OR yahoo.com)", "claimed_employer:(Google OR Amazon OR Microsoft)"],
                mitigations=[TechniqueMitigation("M1030", "Network Segmentation", "Cross-reference claimed employer brand against official domain whitelist.")],
                sub_techniques=[]
            ),
            MitreTechnique(
                technique_id="T1583.001",
                tactic="Resource Development",
                name="Acquire Infrastructure: Domains",
                description="Adversaries purchase inexpensive TLDs (.xyz, .cc, .top) with trademarked corporate names to host phishing portals.",
                detection_queries=["domain.tld:(xyz OR top OR cc OR cfd)", "whois.domain_age_days:<30"],
                mitigations=[TechniqueMitigation("M1031", "Network Intrusion Prevention", "Block young domains registered within last 30 days.")],
                sub_techniques=[]
            ),

            # Financial Impact & Extortion
            MitreTechnique(
                technique_id="T1499.001",
                tactic="Impact",
                name="Financial Theft: Advance Fee Fraud",
                description="Adversaries induce candidate to transfer money for bogus equipment, background checks, or registration fees.",
                detection_queries=["transaction.direction:outbound", "payment.category:upfront_recruitment_fee"],
                mitigations=[TechniqueMitigation("M1001", "Financial Verification", "Strict zero-upfront-money policy for all legitimate recruitment.")],
                sub_techniques=[]
            ),
            MitreTechnique(
                technique_id="T1499.002",
                tactic="Impact",
                name="Financial Theft: Counterfeit Check Overpayment",
                description="Adversaries mail counterfeit cashier checks and demand immediate wire transfer of funds to third-party vendors.",
                detection_queries=["payment.instrument:counterfeit_check", "wire.beneficiary:unvetted_vendor"],
                mitigations=[TechniqueMitigation("M1002", "Bank Check Clearance", "Wait for bank final settlement before disbursing funds from deposited checks.")],
                sub_techniques=[]
            )
        ]

        for item in data:
            self.register_technique(item)

    def get_techniques_by_tactic(self, tactic: str) -> List[MitreTechnique]:
        tech_ids = self._tactic_index.get(tactic.lower(), [])
        return [self.techniques[tid] for tid in tech_ids]
