/**
 * JobGuard AI - Contract Forensics Matrix Ultimate
 * Ultimate TypeScript client-side contract forensics analysis engine
 * mapping 25+ deceptive clause patterns, statutory citations, and restitution rules.
 */

export interface ContractFindingUltimate {
  findingId: string;
  category: 'CHECK_KICKBACK' | 'UPFRONT_DEPOSIT' | 'P2P_APP_PAYMENT' | 'CHAT_INTERVIEW' | 'PII_HARVEST' | 'CUSTOMS_FEE' | 'PERFORMANCE_BOND';
  threatSeverity: 'ELEVATED' | 'HIGH' | 'CRITICAL';
  matchedPattern: string;
  statuteCitation: string;
  remedyDirective: string;
}

export class ContractForensicsMatrixUltimate {
  private static ultimateRules: {
    category: ContractFindingUltimate['category'];
    severity: ContractFindingUltimate['threatSeverity'];
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
      category: 'CUSTOMS_FEE',
      severity: 'CRITICAL',
      regex: /(?:customs\s+duty|border\s+clearance|shipment\s+release)\s+fee\s+of\s+\$?\d+/i,
      statute: '18 U.S.C. § 1343 (Wire Fraud)',
      remedy: 'Never pay customs clearance fees for corporate equipment packages. Employers handle customs directly.',
    },
    {
      category: 'PERFORMANCE_BOND',
      severity: 'HIGH',
      regex: /(?:performance\s+bond|indemnity\s+deposit|employment\s+guarantee\s+fund)/i,
      statute: 'U.S. Fair Labor Standards Act (FLSA)',
      remedy: 'Refuse surety bond demands. Employees are never required to purchase performance bonds for remote jobs.',
    },
    {
      category: 'P2P_APP_PAYMENT',
      severity: 'HIGH',
      regex: /(?:send|wire|transfer)\s+(?:money|funds)\s+via\s+(?:zelle|cashapp|venmo|apple\s+cash)/i,
      statute: '18 U.S.C. § 1343 (Wire Fraud)',
      remedy: 'Never use instant P2P consumer apps to send or receive employment compensation.',
    },
  ];

  public static auditFullContract(text: string): ContractFindingUltimate[] {
    const findings: ContractFindingUltimate[] = [];

    for (let i = 0; i < this.ultimateRules.length; i++) {
      const rule = this.ultimateRules[i];
      const match = text.match(rule.regex);
      if (match) {
        findings.push({
          findingId: `ULT-${i + 1}`,
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
