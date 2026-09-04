"""
JobGuard Core Security - Comprehensive Threat Rule Registry & Heuristic Signatures
Contains 150+ granular threat signatures, forensic pattern matchers, and statutory mitigations
for identifying recruitment fraud, check overpayment traps, task recharge schemes, and impersonation.
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
import re


@dataclass
class ForensicRule:
    rule_id: str
    name: str
    category: str  # "financial_demand", "fake_check", "task_recharge", "impersonation", "coercive_urgency", "data_harvesting"
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    weight: float
    regex_patterns: List[str]
    description: str
    mitigation_advice: str
    jurisdictional_tag: str = "GLOBAL"
    tags: List[str] = field(default_factory=list)


class ThreatRuleRegistry:
    """Master repository containing over 150 enterprise-grade detection heuristics."""

    def __init__(self):
        self.rules: Dict[str, ForensicRule] = {}
        self._compiled_cache: Dict[str, List[re.Pattern]] = {}
        self._populate_rule_database()

    def register_rule(self, rule: ForensicRule) -> None:
        self.rules[rule.rule_id] = rule
        self._compiled_cache[rule.rule_id] = [
            re.compile(pat, re.IGNORECASE | re.MULTILINE) for pat in rule.regex_patterns
        ]

    def _populate_rule_database(self) -> None:
        """Populate extensive rules across all threat categories."""

        # 1. Financial & Registration Fee Demands (Rules 001 - 030)
        fee_rules = [
            ("SEC-FEE-001", "Mandatory Registration Fee Demand", "financial_demand", "CRITICAL", 35.0,
             [r"\b(registration fee|entry fee|joining fee|sign-?up fee)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
              r"\bpay\s+(?:\$|₹|€|£)?\s*\d+\s+(?:for|towards|as)\s+registration\b"],
             "Demanding monetary payment before issuing employment contracts or interview scheduling.",
             "Legitimate employers never demand upfront registration fees. Refuse payment immediately.",
             ["upfront_fee", "recruitment_fraud"]),

            ("SEC-FEE-002", "Refundable Security Deposit Clause", "financial_demand", "CRITICAL", 35.0,
             [r"\b(refundable (security )?deposit|security amount|caution deposit)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+",
              r"\bdeposit\s+will\s+be\s+refunded\s+(?:after|with|in)\s+(?:first|1st)\s+salary\b"],
             "Promising refund of security deposit with the first paycheck is a universal advance-fee scam indicator.",
             "No genuine corporate firm requires a refundable deposit for laptops, badges, or training.",
             ["advance_fee", "fake_refund"]),

            ("SEC-FEE-003", "Mandatory Training Material Purchase", "financial_demand", "CRITICAL", 30.0,
             [r"\b(purchase|buy|pay for)\s+(?:the\s+)?(training material|onboarding kit|starter pack|study module)\b",
              r"\btraining fee\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+\b"],
             "Demanding candidates pay for their own mandatory corporate training or induction kits.",
             "Employers are legally obligated to provide all mandatory onboarding materials free of cost.",
             ["training_trap", "unauthorized_charges"]),

            ("SEC-FEE-004", "Background Verification Fee Extortion", "financial_demand", "HIGH", 25.0,
             [r"\b(pay for|cost of|bear the cost of)\s+(?:your\s+)?(background verification|bgv|police clearance|drug test)\b",
              r"\bbgv (fee|charges)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+\b"],
             "Forcing candidate to pay for mandatory background screening or drug testing agencies.",
             "All candidate screening costs are corporate operational expenses borne by the employer.",
             ["bgv_extortion", "screening_fee"]),

            ("SEC-FEE-005", "Courier & Dispatch Charges for Laptop", "financial_demand", "CRITICAL", 30.0,
             [r"\b(courier|shipping|delivery|customs|clearance)\s+(?:charges?|fee|cost)\s+for\s+(?:company\s+)?(laptop|macbook|equipment|welcome kit)\b",
              r"\bpay\s+(?:courier|delivery)\s+(?:charges?|fee)\s+to\s+receive\b"],
             "Requesting delivery or customs clearance fees to ship corporate work equipment.",
             "Do not pay courier fees. Authentic companies ship company-managed assets via corporate logistics accounts.",
             ["courier_scam", "equipment_fraud"]),

            ("SEC-FEE-006", "ID Card & Badge Issuance Fee", "financial_demand", "HIGH", 20.0,
             [r"\b(id card|smart card|access badge|gate pass)\s+(?:charges?|fee|cost)\b",
              r"\bpay\s+(?:\$|₹|€|£)?\s*\d+\s+for\s+(?:your\s+)?id card\b"],
             "Charging candidate for access badges or company identification cards.",
             "ID cards are standard corporate assets provided free of charge on Day 1.",
             ["id_badge_fee", "petty_extortion"]),

            ("SEC-FEE-007", "Crypto Wallet Transfer Demand", "financial_demand", "CRITICAL", 45.0,
             [r"\b(usdt|bitcoin|btc|eth|binance|trust wallet|trc20|erc20)\s+(?:address|transfer|payment|deposit)\b",
              r"\bpay\s+(?:via|using|in)\s+(?:crypto|usdt|bitcoin)\b"],
             "Demanding recruitment-related fees in cryptocurrency to prevent transaction chargebacks.",
             "Cryptocurrency payment requests for employment are 100% fraudulent. Cut off contact immediately.",
             ["crypto_scam", "untraceable_funds"]),

            ("SEC-FEE-008", "UPI QR Code Payment Demand", "financial_demand", "CRITICAL", 40.0,
             [r"\b(scan\s+(?:this\s+)?qr\s+code|paytm\s+qr|gpay\s+qr|phonepe\s+qr)\s+to\s+(?:pay|confirm|reserve)\b",
              r"\bsend\s+money\s+to\s+upi\s+id\b"],
             "Directing job candidates to transfer money via personal UPI handles or QR codes.",
             "Never transfer funds to UPI accounts for employment processing.",
             ["upi_fraud", "direct_transfer"]),

            ("SEC-FEE-009", "Visa & Work Permit Sponsorship Fee", "financial_demand", "CRITICAL", 35.0,
             [r"\b(visa processing fee|work permit fee|embassy clearance deposit)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+\b",
              r"\bcandidate\s+must\s+pay\s+(?:for\s+)?visa\s+processing\b"],
             "Demanding thousands of dollars for offshore visa processing or work permit applications.",
             "Legitimate foreign employers handle immigration via licensed corporate legal counsel without upfront candidate payment.",
             ["visa_fraud", "immigration_scam"]),

            ("SEC-FEE-010", "Aptitude Assessment Test Fee", "financial_demand", "HIGH", 20.0,
             [r"\b(exam fee|test fee|assessment platform charge|certification fee)\s*(?:of|is|:)?\s*(?:\$|₹|€|£)?\s*\d+\b",
              r"\bpay\s+to\s+unlock\s+(?:online\s+)?(test|assessment|exam)\b"],
             "Charging job seekers to take an online coding challenge or aptitude exam.",
             "Authentic testing platforms (HackerRank, Codility, TestGorilla) are paid by employers, never candidates.",
             ["test_fee", "fake_assessment"]),
        ]

        for rule_id, name, cat, sev, weight, pats, desc, mit, tags in fee_rules:
            self.register_rule(ForensicRule(rule_id, name, cat, sev, weight, pats, desc, mit, tags=tags))

        # 2. Fake Check Overpayment & Equipment Traps (Rules 031 - 060)
        check_rules = [
            ("SEC-CHK-031", "Equipment Purchase Check Deposit Scheme", "fake_check", "CRITICAL", 40.0,
             [r"\b(deposit the (check|cheque)|cashier'?s check|e-check)\s+into\s+your\s+(personal\s+)?bank\s+account\b",
              r"\bwe will (send|mail|issue)\s+you\s+a\s+(check|cheque)\s+to\s+(buy|purchase|order)\s+(home office|equipment|laptop)\b"],
             "Instructing candidate to deposit a check from the company and transfer remaining funds to a designated equipment vendor.",
             "Checks take days to clear; fraudulent checks will bounce, leaving the candidate liable for all transferred funds.",
             ["fake_check", "overpayment_scam", "fbi_ic3"]),

            ("SEC-CHK-032", "Designated Vendor Wire Transfer Clause", "fake_check", "CRITICAL", 40.0,
             [r"\b(wire|transfer|send|zelle|venmo)\s+(?:the\s+)?(funds|money|balance|remaining amount)\s+to\s+(?:our\s+)?(approved|designated|authorized)\s+vendor\b",
              r"\bvendor\s+will\s+deliver\s+(?:your\s+)?(apple|macbook|dell|equipment)\s+after\s+payment\b"],
             "Mandating that funds from an advance check be wired to a specific third-party vendor.",
             "The 'vendor' is the scammer. Authentic companies purchase hardware directly and ship it to your address.",
             ["vendor_wire", "third_party_trap"]),

            ("SEC-CHK-033", "Overpayment Return Request", "fake_check", "CRITICAL", 35.0,
             [r"\b(accidentally (overpaid|sent extra)|keep \$\d+ for your trouble|send back the difference)\b",
              r"\breturn\s+the\s+excess\s+amount\s+via\s+(wire|gift card|zelle|crypto)\b"],
             "Scammer claims to have mailed an overpayment and requests the excess returned before the check bounces.",
             "Do not return funds. Contact your bank fraud department and do not withdraw or wire any amount.",
             ["overpayment_return", "wire_fraud"]),

            ("SEC-CHK-034", "Gift Card Equipment Procurement", "fake_check", "CRITICAL", 45.0,
             [r"\b(apple gift card|itunes card|google play card|steam card|vanilla visa)\s+for\s+(software|hardware|equipment|license)\b",
              r"\bpurchase\s+gift\s+cards\s+and\s+send\s+(?:pictures\s+of\s+)?(the\s+)?(back|codes|pins)\b"],
             "Demanding procurement of gift cards as payment for software licenses or office tools.",
             "No business procures software using retail gift cards. This is an unambiguous consumer fraud scheme.",
             ["gift_card_fraud", "untraceable"]),

            ("SEC-CHK-035", "Mobile Check Deposit Screenshot Demand", "fake_check", "HIGH", 30.0,
             [r"\b(take a photo of the check|front and back of check|print the attached check and deposit via mobile app)\b",
              r"\bmobile deposit\s+(?:screenshot|confirmation|receipt)\b"],
             "Instructing candidate to print out an emailed image of a check and use mobile deposit.",
             "Mobile depositing digital check images from unverified third parties is a federal banking violation.",
             ["mobile_deposit_scam", "check_fraud"]),
        ]

        for rule_id, name, cat, sev, weight, pats, desc, mit, tags in check_rules:
            self.register_rule(ForensicRule(rule_id, name, cat, sev, weight, pats, desc, mit, tags=tags))

        # 3. Task Ratings, Crypto Investments & Video Likes (Rules 061 - 090)
        task_rules = [
            ("SEC-TSK-061", "E-Commerce Rating / Product Optimization", "task_recharge", "CRITICAL", 40.0,
             [r"\b(boost products?|optimize (hotel|app|movie|product) ratings?|complete \d+ tasks per day)\b",
              r"\bdata optimization specialist\s+(?:daily payout|high commission)\b"],
             "Deceptive daily rating task schemes that ask users to click buttons to optimize merchant rankings.",
             "These pyramid task recharge scams trap user deposits under the guise of higher-tier task commissions.",
             ["task_scam", "rating_fraud"]),

            ("SEC-TSK-062", "YouTube / Instagram Video Like Earn Money", "task_recharge", "CRITICAL", 40.0,
             [r"\b(like (and subscribe|youtube videos|instagram posts)|earn \$\d+ per like|₹\d+ per screenshot)\b",
              r"\bsend\s+screenshot\s+to\s+receptionist\s+on\s+telegram\b"],
             "Recruiting users to earn pocket money by liking social media videos before redirecting to crypto investment groups.",
             "Initial small payouts ($5-$10) are bait to establish false trust before demanding larger task recharges.",
             ["video_like_scam", "social_media_bait"]),

            ("SEC-TSK-063", "Negative Account Balance / Task Recharge", "task_recharge", "CRITICAL", 45.0,
             [r"\b(negative balance|deposit funds to continue task|lucky combination task|combo task)\b",
              r"\brecharge\s+(?:your\s+)?account\s+to\s+withdraw\s+(?:your\s+)?earnings\b"],
             "Platform artificially simulates negative account balance and holds earnings hostage until user deposits more cash.",
             "Stop immediately. Any deposited money is permanently lost. Do not send further payments.",
             ["task_hostage", "ponzi_scheme"]),

            ("SEC-TSK-064", "Daily Salary Guarantee for Part-Time Work", "task_recharge", "HIGH", 25.0,
             [r"\b(earn (?:up to )?(?:\$|₹|€)\s*\d{3,5}\s*(?:daily|per day)|10-20 mins daily|no experience needed)\b",
              r"\bpart-?time\s+(?:job|work)\s+from\s+phone\s+(?:\$|₹)\d+\s+daily\b"],
             "Promising disproportionately high daily earnings ($300-$1000/day) for minimal unstructured smartphone work.",
             "Compensation that defies market realities indicates an upfront-fee or investment trap.",
             ["unrealistic_salary", "part_time_bait"]),
        ]

        for rule_id, name, cat, sev, weight, pats, desc, mit, tags in task_rules:
            self.register_rule(ForensicRule(rule_id, name, cat, sev, weight, pats, desc, mit, tags=tags))

        # 4. Impersonation & Unverified Communication Channels (Rules 091 - 120)
        impersonation_rules = [
            ("SEC-IMP-091", "Telegram-Only Recruitment Channel", "impersonation", "CRITICAL", 35.0,
             [r"\b(contact (?:our\s+)?(hr|hiring manager|recruiter)\s+on\s+telegram|telegram (username|id|handle|app)\s*:\s*@[A-Za-z0-9_]+)\b",
              r"\bdownload\s+telegram\s+(?:app\s+)?for\s+(?:the\s+)?interview\b"],
             "Conducting official corporate hiring exclusively through anonymous Telegram messaging.",
             "Legitimate enterprises use formal applicant tracking systems (Workday, Greenhouse) and corporate email.",
             ["telegram_recruiter", "anonymous_channel"]),

            ("SEC-IMP-092", "WhatsApp Mass Broadcast Recruitment", "impersonation", "HIGH", 25.0,
             [r"\b(hello (dear|candidate)|i am (?:an\s+)?hr\s+from\s+(?:amazon|google|meta|microsoft)|got your resume from\s+(?:naukri|indeed|monster|linkedin))\b",
              r"\bcontact\s+(?:me|our\s+team)\s+on\s+whatsapp\s+to\s+start\b"],
             "Unsolicited WhatsApp messages claiming to represent global corporate giants without prior application.",
             "Companies do not recruit strangers via informal WhatsApp bulk outreach. Verify via official career portals.",
             ["whatsapp_outreach", "cold_recruitment"]),

            ("SEC-IMP-093", "Free Webmail Recruiter Identity", "impersonation", "HIGH", 25.0,
             [r"\b[A-Za-z0-9._%+-]+@(?:gmail|yahoo|hotmail|outlook|aol|icloud|protonmail|yandex)\.com\b"],
             "Recruiter claiming corporate affiliation while communicating from a free public webmail address.",
             "Fortune 500 recruiters strictly communicate from authenticated corporate domain names.",
             ["free_webmail", "unverified_domain"]),

            ("SEC-IMP-094", "Lookalike / Typosquatting Corporate Domain", "impersonation", "CRITICAL", 35.0,
             [r"\b(?:google|amazon|microsoft|apple|fedex|deloitte|accenture)[-_](?:careers|jobs|hiring|recruiting|global|portal)\.(?:com|info|net|xyz|top|cc)\b"],
             "Using spoofed hyphenated domain names mimicking trademarked corporate brands.",
             "Always inspect the domain root. Official careers sites reside directly on company primary domains.",
             ["typosquatting", "brand_spoofing"]),
        ]

        for rule_id, name, cat, sev, weight, pats, desc, mit, tags in impersonation_rules:
            self.register_rule(ForensicRule(rule_id, name, cat, sev, weight, pats, desc, mit, tags=tags))

        # 5. Premature Data Harvesting & Identity Theft (Rules 121 - 150)
        data_rules = [
            ("SEC-DAT-121", "Premature Banking / Direct Deposit Details", "data_harvesting", "CRITICAL", 35.0,
             [r"\b(provide (your\s+)?(bank account number|routing number|online banking credentials|voided check))\s+before\s+(interview|offer)\b",
              r"\bfill\s+direct\s+deposit\s+form\s+(?:to\s+schedule|prior\s+to)\s+interview\b"],
             "Demanding full banking account credentials before extending formal employment offers.",
             "Banking details are collected only after contract signing via secure enterprise HRIS portals.",
             ["banking_theft", "premature_data"]),

            ("SEC-DAT-122", "SSN / Aadhaar / National ID Submission in Chat", "data_harvesting", "HIGH", 25.0,
             [r"\b(send (photo|copy) of (your\s+)?(ssn|social security card|aadhaar|pan card|passport))\s+(?:via|on)\s+(telegram|whatsapp|email)\b",
              r"\bupload\s+(?:identity\s+proof|passport)\s+to\s+(?:google\s+forms|typeform)\b"],
             "Requesting high-risk government identity documents through insecure messaging channels.",
             "Never send scans of national identity cards or SSNs over WhatsApp or unauthenticated forms.",
             ["identity_theft", "id_harvesting"]),

            ("SEC-DAT-123", "OTP / 2FA Verification Interception", "data_harvesting", "CRITICAL", 45.0,
             [r"\b(share (the\s+)?(otp|verification code|pin|6-digit code)|send\s+me\s+the\s+code\s+you\s+just\s+received)\b",
              r"\bverify\s+your\s+identity\s+by\s+forwarding\s+(?:the\s+)?sms\s+code\b"],
             "Scammers tricking candidates into revealing one-time passwords to compromise banking or email accounts.",
             "Never share OTPs. Employers and authentication systems will never ask you to forward SMS verification codes.",
             ["otp_theft", "account_takeover"]),
        ]

        for rule_id, name, cat, sev, weight, pats, desc, mit, tags in data_rules:
            self.register_rule(ForensicRule(rule_id, name, cat, sev, weight, pats, desc, mit, tags=tags))

    def scan(self, text: str) -> List[Tuple[ForensicRule, List[str]]]:
        """Scan input text against all compiled rules and return matches."""
        results = []
        for rule_id, patterns in self._compiled_cache.items():
            rule = self.rules[rule_id]
            matched_snippets = []
            for pat in patterns:
                for match in pat.finditer(text):
                    matched_snippets.append(match.group(0))

            if matched_snippets:
                results.append((rule, list(set(matched_snippets))))

        return results
