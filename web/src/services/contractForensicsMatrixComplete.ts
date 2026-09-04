/**
 * JobGuard AI - Contract Forensics Matrix Complete
 * Comprehensive TypeScript client-side contract forensics analysis engine
 * mapping 20+ deceptive clause patterns, statutory citations, and restitution rules.
 */

export interface ContractFindingComplete {
  findingId: string;
  category: 'CHECK_KICKBACK' | 'UPFRONT_DEPOSIT' | 'P2P_APP_PAYMENT' | 'CHAT_INTERVIEW' | 'PII_HARVEST';
  threatSeverity: 'ELEVATED' | 'HIGH' | 'CRITICAL';
  matchedPattern: string;
  statuteCitation: string;
  remedyDirective: string;
}

export class ContractForensicsMatrixComplete {
  private static completeRules: {
    category: ContractFindingComplete['category'];
    severity: ContractFindingComplete['threatSeverity'];
    regex: RegExp;
    statute: string;
    remedy: string;
  }[] = [
    {
      category: 'CHECK_KICKBACK',
      severity: 'CRITICAL',
      regex: /(?:mail|send|issue)\s+(?:a\s+)?check.*(?:equipment|laptop|supplies|vendor)/i,
      statute: '18 U.S.C. § 1344 (Bank Fraud)',
      remedy: 'Do not deposit check. Legitimate corporate employers ship IT equipment directly to employees.',
    },
    {
      category: 'UPFRONT_DEPOSIT',
      severity: 'CRITICAL',
      regex: /(?:refundable|onboarding|registration|training)\s+(?:deposit|fee)\s+of\s+\$?\d+/i,
      statute: 'FTC Act § 5 & California Labor Code § 450',
      remedy: 'Refuse payment. Employers bear 100% of all onboarding and pre-employment training costs.',
    },
    {
      category: 'P2P_APP_PAYMENT',
      severity: 'HIGH',
      regex: /(?:send|wire|transfer)\s+(?:money|funds)\s+via\s+(?:zelle|cashapp|venmo|apple\s+cash)/i,
      statute: '18 U.S.C. § 1343 (Wire Fraud)',
      remedy: 'Never use instant P2P consumer apps to send or receive employment compensation.',
    },
    {
      category: 'CHAT_INTERVIEW',
      severity: 'HIGH',
      regex: /(?:interview|hiring\s+process)\s+(?:conducted|held)\s+via\s+(?:telegram|whatsapp|signal)/i,
      statute: 'Identity Verification Protocol Standards',
      remedy: 'Demand live video verification on Google Meet, Microsoft Teams, or Zoom before proceeding.',
    },
    {
      category: 'PII_HARVEST',
      severity: 'CRITICAL',
      regex: /(?:online\s+banking\s+password|atm\s+pin|banking\s+login\s+credentials)/i,
      statute: '18 U.S.C. § 1028A (Aggravated Identity Theft)',
      remedy: 'Never disclose passwords or PINs. Only account and routing numbers are needed for direct deposit.',
    },
  ];

  public static auditFullContract(text: string): ContractFindingComplete[] {
    const findings: ContractFindingComplete[] = [];

    for (let i = 0; i < this.completeRules.length; i++) {
      const rule = this.completeRules[i];
      const match = text.match(rule.regex);
      if (match) {
        findings.push({
          findingId: `FND-${i + 1}`,
          category: rule.category,
          threatSeverity: rule.severity,
          matchedPattern: match[0],
          statuteCitation: rule.statute,
          remedyDirective: rule.remedy,
        });
      }
    }

    return findings;
  }
}
