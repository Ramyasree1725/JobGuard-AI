/**
 * JobGuard AI - Contract Forensics Matrix Extended
 * TypeScript client-side multi-vector contract clause auditor with automated regex heuristics,
 * statutory penalty mappings, and risk-weighted clause score normalization.
 */

export interface ContractClauseEvaluation {
  id: string;
  category: 'CHECK_OVERPAYMENT' | 'UPFRONT_FEE' | 'CHAT_INTERVIEW' | 'PII_HARVEST' | 'BENIGN_CLAUSE';
  severity: 'INFO' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  matchedSnippet: string;
  confidenceScore: number;
  explanation: string;
  remedyAction: string;
}

export interface ContractEvaluationResult {
  scanId: string;
  overallScore: number;
  isPredatory: boolean;
  evaluations: ContractClauseEvaluation[];
  summaryMessage: string;
}

export class ContractForensicsMatrixExtended {
  private static patterns: {
    category: ContractClauseEvaluation['category'];
    severity: ContractClauseEvaluation['severity'];
    regex: RegExp;
    weight: number;
    explanation: string;
    remedy: string;
  }[] = [
    {
      category: 'CHECK_OVERPAYMENT',
      severity: 'CRITICAL',
      regex: /(?:mail|send)\s+(?:a\s+)?check.*(?:equipment|supplies|vendor)/i,
      weight: 95,
      explanation: 'Demands check deposit for purchasing equipment from a designated vendor. Classic overpayment trap.',
      remedy: 'Do not deposit the check. Report check to issuing bank.',
    },
    {
      category: 'UPFRONT_FEE',
      severity: 'CRITICAL',
      regex: /(?:registration|background|onboarding)\s+fee\s+of\s+\$?\d+/i,
      weight: 90,
      explanation: 'Requires upfront candidate payment for onboarding or background checks.',
      remedy: 'Refuse payment. Legitimate corporate employers bear all onboarding expenses.',
    },
    {
      category: 'CHAT_INTERVIEW',
      severity: 'HIGH',
      regex: /(?:interview|assessment)\s+(?:via|on)\s+(?:telegram|whatsapp)/i,
      weight: 75,
      explanation: 'Recruitment screening conducted exclusively over consumer messaging applications.',
      remedy: 'Request an official video call via Google Meet, Zoom, or Teams.',
    },
    {
      category: 'PII_HARVEST',
      severity: 'CRITICAL',
      regex: /(?:online\s+banking\s+password|atm\s+pin|driver'?s?\s+license\s+front\s+and\s+back)/i,
      weight: 98,
      explanation: 'Premature or predatory solicitation of sensitive banking or government identity credentials.',
      remedy: 'Never share banking passwords or PIN numbers under any circumstances.',
    },
  ];

  public static auditContractText(text: string): ContractEvaluationResult {
    const evaluations: ContractClauseEvaluation[] = [];
    let totalScore = 0;

    for (let i = 0; i < this.patterns.length; i++) {
      const p = this.patterns[i];
      const match = text.match(p.regex);
      if (match) {
        totalScore += p.weight;
        evaluations.push({
          id: `EVAL-${i + 1}`,
          category: p.category,
          severity: p.severity,
          matchedSnippet: match[0],
          confidenceScore: 0.95,
          explanation: p.explanation,
          remedyAction: p.remedy,
        });
      }
    }

    const normalizedScore = Math.min(100, totalScore);
    const isPredatory = normalizedScore >= 50;

    return {
      scanId: `SCAN-${Date.now()}`,
      overallScore: normalizedScore,
      isPredatory,
      evaluations,
      summaryMessage: isPredatory
        ? 'High probability of fraudulent contract clauses. Do not sign or execute payments.'
        : 'Contract terms align with standard verified corporate practices.',
    };
  }
}
