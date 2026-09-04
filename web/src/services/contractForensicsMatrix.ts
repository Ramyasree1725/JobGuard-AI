/**
 * JobGuard Web Architecture - Extended Contract Forensics & Clause Risk Matrix
 * Real-time parsing of legal clauses with statutory references and visual status indicators.
 */

export interface ClauseAuditItem {
  id: string;
  clauseTitle: string;
  rawClauseText: string;
  isCompliant: boolean;
  violationCategory?: string;
  statutoryReference?: string;
  suggestedAction: string;
}

export class ContractForensicsMatrix {
  public static parseOfferDocument(fullText: string): ClauseAuditItem[] {
    const lines = fullText.split('\n').filter((l) => l.trim().length > 10);
    const items: ClauseAuditItem[] = [];

    lines.forEach((line, i) => {
      const lineLower = line.toLowerCase();
      let compliant = true;
      let category: string | undefined;
      let statute: string | undefined;
      let action = 'Clause is standard and adheres to normal business practices.';

      if (lineLower.includes('registration fee') || lineLower.includes('security deposit')) {
        compliant = false;
        category = 'Unlawful Upfront Payment Demand';
        statute = 'Section 66D IT Act / US FTC Act § 5';
        action = 'Do not pay any fee. Legitimate employers bear all recruitment costs.';
      } else if (lineLower.includes('check') || lineLower.includes('wire to vendor')) {
        compliant = false;
        category = 'Counterfeit Check Equipment Scheme';
        statute = '18 U.S.C. § 1343 (Wire Fraud)';
        action = 'Never wire money received from a mailed check.';
      } else if (lineLower.includes('urgent') || lineLower.includes('within 24 hours')) {
        compliant = false;
        category = 'Artificial Coercive Pressure';
        statute = 'Fair Work Practice Standard';
        action = 'Request a formal 3-5 day review window before taking action.';
      }

      items.push({
        id: `CLAUSE-${i + 1}`,
        clauseTitle: `Clause §${i + 1}`,
        rawClauseText: line.trim(),
        isCompliant: compliant,
        violationCategory: category,
        statutoryReference: statute,
        suggestedAction: action,
      });
    });

    return items;
  }
}
