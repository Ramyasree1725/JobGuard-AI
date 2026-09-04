/**
 * JobGuard Web Architecture - Client-Side Contract Forensics & Clause Analyzer
 * Parses contract paragraphs, flags predatory fee clauses, and produces structured risk badges.
 */

export interface ContractClauseAudit {
  clauseIndex: number;
  originalText: string;
  isFlaggedRisk: boolean;
  threatCategory: string;
  riskSeverity: 'CRITICAL' | 'WARNING' | 'SAFE';
  remediationAdvice: string;
}

export class ContractForensicsAnalyzer {
  public static auditParagraphs(contractText: string): ContractClauseAudit[] {
    const paragraphs = contractText.split(/\n\s*\n/).filter((p) => p.trim().length > 15);
    const audits: ContractClauseAudit[] = [];

    paragraphs.forEach((p, idx) => {
      const pLower = p.toLowerCase();
      let flagged = false;
      let category = 'Standard Employment Clause';
      let severity: 'CRITICAL' | 'WARNING' | 'SAFE' = 'SAFE';
      let advice = 'Clause conforms to standard corporate hiring norms.';

      if (pLower.includes('registration fee') || pLower.includes('security deposit') || pLower.includes('pay')) {
        flagged = true;
        category = 'Advance Fee / Registration Trap';
        severity = 'CRITICAL';
        advice = 'Legitimate employers never charge candidates. Do not send payment.';
      } else if (pLower.includes('check') || pLower.includes('wire') || pLower.includes('vendor')) {
        flagged = true;
        category = 'Fake Check Equipment Deposit';
        severity = 'CRITICAL';
        advice = 'Fake checks bounce after 3-5 days. Never forward money to an unvetted vendor.';
      } else if (pLower.includes('urgent') || pLower.includes('expire') || pLower.includes('forfeit')) {
        flagged = true;
        category = 'Artificial Coercive Pressure';
        severity = 'WARNING';
        advice = 'Take time to independently verify recruiter credentials on LinkedIn.';
      }

      audits.push({
        clauseIndex: idx + 1,
        originalText: p.trim(),
        isFlaggedRisk: flagged,
        threatCategory: category,
        riskSeverity: severity,
        remediationAdvice: advice,
      });
    });

    return audits;
  }
}
