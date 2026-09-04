/**
 * JobGuard Web Architecture - Deep Client-Side Threat Correlation Engine
 * Correlates linguistic pressure, fake check markers, and recruiter identity.
 */

export interface DetailedAnalysisBreakdown {
  linguisticScore: number;
  financialDemandScore: number;
  domainTrustScore: number;
  urgencyScore: number;
  finalRiskPercentage: number;
  identifiedThreats: string[];
}

export class DeepAnalysisEngine {
  public static analyzeContractText(rawText: string, recruiterEmail: string): DetailedAnalysisBreakdown {
    const textLower = rawText.toLowerCase();
    const threats: string[] = [];

    let finScore = 0;
    if (textLower.includes('registration fee') || textLower.includes('security deposit') || textLower.includes('pay')) {
      finScore += 45;
      threats.push('Upfront Financial Fee Demanded');
    }
    if (textLower.includes('check') || textLower.includes('cheque') || textLower.includes('wire transfer')) {
      finScore += 45;
      threats.push('Counterfeit Check / Equipment Vendor Wire Scheme');
    }

    let urgencyScore = 0;
    if (textLower.includes('urgent') || textLower.includes('immediately') || textLower.includes('today only')) {
      urgencyScore += 30;
      threats.push('High-Pressure Psychological Coercion');
    }

    let domainScore = 0;
    if (recruiterEmail.includes('@gmail.com') || recruiterEmail.includes('@yahoo.com') || recruiterEmail.includes('@outlook.com')) {
      domainScore += 25;
      threats.push('Unverified Free Webmail Provider Used by Purported Recruiter');
    }

    const total = Math.min(100, finScore + urgencyScore + domainScore);

    return {
      linguisticScore: Math.round(urgencyScore * 1.5),
      financialDemandScore: finScore,
      domainTrustScore: domainScore,
      urgencyScore,
      finalRiskPercentage: total,
      identifiedThreats: threats,
    };
  }
}
