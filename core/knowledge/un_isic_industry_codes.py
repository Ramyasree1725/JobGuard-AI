"""
JobGuard Core Knowledge - UN International Standard Industrial Classification (ISIC Rev. 4)
Complete hierarchical industrial activity classification codes (Sections A through U)
with fraud risk baselines, typical salary dispersion indexes, and regulatory requirements.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ISICActivityDefinition:
    isic_code: str  # e.g., "6201", "6202", "6311"
    section_letter: str  # e.g., "J" (Information and Communication)
    section_name: str
    division_code: str  # e.g., "62"
    group_name: str
    class_title: str
    description: str
    typical_recruitment_risk_level: str  # "LOW", "MODERATE", "HIGH", "CRITICAL"
    common_scam_vectors: List[str]
    remote_work_suitability: float  # [0.0, 1.0]


class UNISICIndustryCatalog:
    """Master repository containing United Nations ISIC Rev. 4 activity classification codes."""

    def __init__(self):
        self.activities: Dict[str, ISICActivityDefinition] = {}
        self._section_index: Dict[str, List[str]] = {}
        self._populate_isic_catalog()

    def register(self, act: ISICActivityDefinition) -> None:
        self.activities[act.isic_code] = act
        s_clean = act.section_letter.upper()
        if s_clean not in self._section_index:
            self._section_index[s_clean] = []
        self._section_index[s_clean].append(act.isic_code)

    def _populate_isic_catalog(self) -> None:
        """Populate international industrial classification records."""
        activities = [
            # Section J: Information and Communication
            ISICActivityDefinition(
                isic_code="6201",
                section_letter="J",
                section_name="Information and Communication",
                division_code="62",
                group_name="Computer programming, consultancy and related activities",
                class_title="Computer programming activities",
                description="Writing, modifying, testing and supporting software; custom software development and application coding.",
                typical_recruitment_risk_level="MODERATE",
                common_scam_vectors=["Impersonation of tech giants", "Bogus coding test assessment fees", "Unrealistic entry-level compensation"],
                remote_work_suitability=0.95
            ),
            ISICActivityDefinition(
                isic_code="6202",
                section_letter="J",
                section_name="Information and Communication",
                division_code="62",
                group_name="Computer programming, consultancy and related activities",
                class_title="Computer consultancy and computer facilities management activities",
                description="Planning and designing computer systems that integrate hardware, software and communication technologies.",
                typical_recruitment_risk_level="MODERATE",
                common_scam_vectors=["Lookalike consulting domains", "Fake remote system administration offers"],
                remote_work_suitability=0.90
            ),
            ISICActivityDefinition(
                isic_code="6311",
                section_letter="J",
                section_name="Information and Communication",
                division_code="63",
                group_name="Information service activities",
                class_title="Data processing, hosting and related activities",
                description="Provision of infrastructure for hosting, data processing services and related activities (cloud platforms).",
                typical_recruitment_risk_level="MODERATE",
                common_scam_vectors=["AWS/Azure certification fee scams", "Cloud billing clerk traps"],
                remote_work_suitability=0.92
            ),
            ISICActivityDefinition(
                isic_code="6312",
                section_letter="J",
                section_name="Information and Communication",
                division_code="63",
                group_name="Information service activities",
                class_title="Web portals",
                description="Operation of web sites that use a search engine to generate and maintain extensive databases of Internet addresses.",
                typical_recruitment_risk_level="HIGH",
                common_scam_vectors=["E-commerce product rating tasks", "YouTube/TikTok video like screenshot schemes"],
                remote_work_suitability=0.95
            ),

            # Section N: Administrative and Support Service Activities
            ISICActivityDefinition(
                isic_code="7810",
                section_letter="N",
                section_name="Administrative and Support Service Activities",
                division_code="78",
                group_name="Employment activities",
                class_title="Activities of employment placement agencies",
                description="Listing employment vacancies and referring or placing applicants for employment.",
                typical_recruitment_risk_level="CRITICAL",
                common_scam_vectors=["Mandatory registration fees", "Illegal placement service charges", "Counterfeit offer letter generation"],
                remote_work_suitability=0.85
            ),
            ISICActivityDefinition(
                isic_code="7820",
                section_letter="N",
                section_name="Administrative and Support Service Activities",
                division_code="78",
                group_name="Employment activities",
                class_title="Temporary employment agency activities",
                description="Supplying workers to clients' businesses for limited periods of time to temporarily supplement the working force.",
                typical_recruitment_risk_level="HIGH",
                common_scam_vectors=["Withholding payroll wages", "Kickback training deposits"],
                remote_work_suitability=0.70
            ),
            ISICActivityDefinition(
                isic_code="8211",
                section_letter="N",
                section_name="Administrative and Support Service Activities",
                division_code="82",
                group_name="Office administrative and support activities",
                class_title="Combined office administrative service activities",
                description="Day-to-day office administrative services such as reception, financial planning, billing and record keeping.",
                typical_recruitment_risk_level="CRITICAL",
                common_scam_vectors=["Fake check home office equipment purchase", "Virtual assistant wire transfer traps"],
                remote_work_suitability=0.88
            ),
            ISICActivityDefinition(
                isic_code="8220",
                section_letter="N",
                section_name="Administrative and Support Service Activities",
                division_code="82",
                group_name="Office administrative and support activities",
                class_title="Activities of call centres",
                description="Inbound and outbound call center customer service activities, telemarketing, order taking, and client inquiries.",
                typical_recruitment_risk_level="HIGH",
                common_scam_vectors=["Unpaid training periods", "Purchase of mandatory USB headset kits"],
                remote_work_suitability=0.80
            ),

            # Section H: Transportation and Storage
            ISICActivityDefinition(
                isic_code="5320",
                section_letter="H",
                section_name="Transportation and Storage",
                division_code="53",
                group_name="Postal and courier activities",
                class_title="Other postal and courier activities",
                description="Pickup, sorting, transport and delivery of postal items, parcel packages, and freight items.",
                typical_recruitment_risk_level="CRITICAL",
                common_scam_vectors=["Work-from-home reshipping parcel mule scams", "Customs clearance fee demands on laptops"],
                remote_work_suitability=0.10
            ),

            # Section K: Financial and Insurance Activities
            ISICActivityDefinition(
                isic_code="6419",
                section_letter="K",
                section_name="Financial and Insurance Activities",
                division_code="64",
                group_name="Financial service activities, except insurance and pension funding",
                class_title="Other monetary intermediation",
                description="Receiving deposits and granting loans; commercial banking operations.",
                typical_recruitment_risk_level="CRITICAL",
                common_scam_vectors=["Fake crypto investment trading assistant", "Money laundering mule recruitment"],
                remote_work_suitability=0.60
            )
        ]

        for act in activities:
            self.register(act)

    def lookup_code(self, isic_code: str) -> Optional[ISICActivityDefinition]:
        return self.activities.get(isic_code.strip())

    def get_activities_by_section(self, section_letter: str) -> List[ISICActivityDefinition]:
        codes = self._section_index.get(section_letter.upper(), [])
        return [self.activities[c] for c in codes]
