/**
 * JobGuard AI - Contract Forensics Matrix Master
 * Client-side master contract forensics scanner mapping clause patterns,
 * legal statute citations, and financial kickback threat categories.
 */

export interface MasterContractFinding {
  ruleCode: string;
  category: 'CHECK_FRAUD' | 'UPFRONT_FEE' | 'CHAT_HIRING' | 'PII_THEFT' | 'BENIGN_STANDARD';
  riskRating: 'SAFE' | 'ELEVATED' | 'CRITICAL';
  matchedText: string;
  legalStatuteRef: string;
  advisoryNote: string;
}

export class ContractForensicsMatrixMaster {
  private static masterRules: {
    ruleCode: string;
    category: MasterContractFinding['category'];
    riskRating: MasterContractFinding['riskRating'];
    regex: RegExp;
    statute: string;
    advice: string;
  }[] = [
    {
      ruleCode: 'MTR-001',
      category: 'CHECK_FRAUD',
      riskRating: 'CRITICAL',
      regex: /(?:check|cheque)\s+(?:will\s+be\s+sent|mailed|issued)\s+for\s+(?:equipment|supplies|laptop)/i,
      statute: '18 U.S. Code § 1344 - Bank Fraud',
      advice: 'Never deposit a check sent by an employer to buy equipment from a third-party vendor.',
    },
    {
      ruleCode: 'MTR-002',
      category: 'CHECK_FRAUD',
      riskRating: 'CRITICAL',
      regex: /(?:wire|forward|send)\s+(?:surplus|excess|remaining\s+funds)\s+to\s+(?:vendor|supplier)/i,
      statute: '18 U.S. Code § 1343 - Wire Fraud',
      advice: 'Refuse all wire kickback instructions. Candidate is personally liable for bounced check funds.',
    },
    {
      ruleCode: 'MTR-003',
      category: 'UPFRONT_FEE',
      riskRating: 'CRITICAL',
      regex: /(?:refundable|security|onboarding|registration)\s+(?:deposit|fee)\s+of\s+\$?\d+/i,
      statute: 'FTC Act Section 5 & California Labor Code § 450',
      advice: 'Genuine employers never require candidate payment for onboarding or background checks.',
    },
    {
      ruleCode: 'MTR-004',
      category: 'CHAT_HIRING',
      riskRating: 'ELEVATED',
      regex: /(?:interview|screening)\s+(?:on|via|through)\s+(?:telegram|whatsapp|signal)/i,
      statute: 'Industry Best Practice - Synchronous Identity Verification',
      advice: 'Insist on a verified video conference (Google Meet / Zoom / Teams) with cameras turned on.',
    },
    {
      ruleCode: 'MTR-005',
      category: 'PII_THEFT',
      riskRating: 'CRITICAL',
      regex: /(?:online\s+banking\s+password|atm\s+pin|banking\s+login\s+credentials)/i,
      statute: '18 U.S. Code § 1028 - Aggravated Identity Theft',
      advice: 'Never disclose online banking passwords. Employers only need direct deposit routing numbers.',
    },
  ];

  public static auditDocument(contractText: string): MasterContractFinding[] {
    const findings: MasterContractFinding[] = [];

    for (const rule of this.masterRules) {
      const match = contractText.match(rule.regex);
      if (match) {
        findings.push({
          ruleCode: rule.ruleCode,
          category: rule.category,
          riskRating: rule.riskRating,
          matchedText: match[0],
          legalStatuteRef: rule.statute,
          advisoryNote: rule.advice,
        });
      }
    }

    return findings;
  }
}
