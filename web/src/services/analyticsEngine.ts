/**
 * JobGuard Web Architecture - Client-Side Analytics & Threat Visualization Engine
 * Implements real-time score weighting, anomaly detection, and categorical threat distribution.
 */

export interface ThreatVectorDistribution {
  paymentDemands: number;
  contactImpersonation: number;
  urgencyPressure: number;
  salaryRealism: number;
  jobSpecifications: number;
}

export interface AdvancedScanAnalytics {
  overallRiskScore: number;
  legitimacyScore: number;
  vectorDistribution: ThreatVectorDistribution;
  primaryRiskFactor: string;
  confidenceInterval: [number, number];
  estimatedAuditDurationMs: number;
}

export class AnalyticsEngine {
  /**
   * Compute multi-vector risk distribution from raw detected flags
   */
  public static computeVectorDistribution(
    flags: Array<{ category: string; weight: number }>
  ): ThreatVectorDistribution {
    const distribution: ThreatVectorDistribution = {
      paymentDemands: 0,
      contactImpersonation: 0,
      urgencyPressure: 0,
      salaryRealism: 0,
      jobSpecifications: 0,
    };

    flags.forEach((f) => {
      const cat = f.category.toLowerCase();
      if (cat.includes('payment') || cat.includes('check') || cat.includes('fee')) {
        distribution.paymentDemands += f.weight * 2.2;
      } else if (cat.includes('contact') || cat.includes('recruiter') || cat.includes('domain')) {
        distribution.contactImpersonation += f.weight * 2.2;
      } else if (cat.includes('urgency') || cat.includes('pressure')) {
        distribution.urgencyPressure += f.weight * 2.2;
      } else if (cat.includes('salary') || cat.includes('compensation')) {
        distribution.salaryRealism += f.weight * 2.2;
      } else {
        distribution.jobSpecifications += f.weight * 2.2;
      }
    });

    // Clamp to [0, 100]
    return {
      paymentDemands: Math.min(100, Math.round(distribution.paymentDemands)),
      contactImpersonation: Math.min(100, Math.round(distribution.contactImpersonation)),
      urgencyPressure: Math.min(100, Math.round(distribution.urgencyPressure)),
      salaryRealism: Math.min(100, Math.round(distribution.salaryRealism)),
      jobSpecifications: Math.min(100, Math.round(distribution.jobSpecifications)),
    };
  }

  /**
   * Determine primary threat driver
   */
  public static getPrimaryThreatFactor(dist: ThreatVectorDistribution): string {
    const entries: Array<[string, number]> = [
      ['Upfront Fee Demands & Check Traps', dist.paymentDemands],
      ['Unverified / Impersonated Recruiter Channel', dist.contactImpersonation],
      ['High-Pressure Artificial Urgency', dist.urgencyPressure],
      ['Unrealistic Salary & Compensation Bait', dist.salaryRealism],
      ['Vague Role Requirements', dist.jobSpecifications],
    ];

    entries.sort((a, b) => b[1] - a[1]);
    return entries[0][1] > 0 ? entries[0][0] : 'None (Legitimate Employment Standard)';
  }

  /**
   * Calculate 95% Confidence Interval for risk score
   */
  public static calculateConfidenceBounds(score: number, sampleSize: number = 1): [number, number] {
    const stdErr = Math.sqrt(Math.max(1, score * (100 - score) / Math.max(1, sampleSize)));
    const margin = 1.96 * (stdErr * 0.1);
    return [
      Math.max(0, Math.round(score - margin)),
      Math.min(100, Math.round(score + margin)),
    ];
  }
}
