/**
 * JobGuard AI - Multivariate Risk Matrix Computer
 * Aggregates threat scores across domain reputation, language urgency, payment mechanics,
 * interview channel legitimacy, and compensation distortions into radar chart metrics.
 */

export interface ThreatVectorMetrics {
  upfrontFeeRisk: number; // 0 - 100
  fakeCheckRisk: number;
  chatInterviewRisk: number;
  salaryAnomalyRisk: number;
  domainSpoofRisk: number;
  piiHarvestRisk: number;
}

export interface RadarDataset {
  labels: string[];
  values: number[];
  aggregateScore: number;
  threatTier: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
}

export class RiskMatrixComputer {
  /**
   * Computes normalized radar polygon dimensions from raw threat detection flags.
   */
  public static computeRadarDimensions(metrics: ThreatVectorMetrics): RadarDataset {
    const labels = [
      'Upfront Fees',
      'Check Overpayment',
      'Chat-Only Hiring',
      'Salary Distortion',
      'Domain Spoofing',
      'PII Harvesting',
    ];

    const values = [
      Math.max(0, Math.min(100, metrics.upfrontFeeRisk)),
      Math.max(0, Math.min(100, metrics.fakeCheckRisk)),
      Math.max(0, Math.min(100, metrics.chatInterviewRisk)),
      Math.max(0, Math.min(100, metrics.salaryAnomalyRisk)),
      Math.max(0, Math.min(100, metrics.domainSpoofRisk)),
      Math.max(0, Math.min(100, metrics.piiHarvestRisk)),
    ];

    // Weighted aggregate score calculation
    const weights = [0.25, 0.25, 0.15, 0.10, 0.15, 0.10];
    let weightedSum = 0;
    for (let i = 0; i < values.length; i++) {
      weightedSum += values[i] * weights[i];
    }

    const aggregateScore = Math.round(weightedSum);

    let threatTier: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL' = 'LOW';
    if (aggregateScore >= 75) {
      threatTier = 'CRITICAL';
    } else if (aggregateScore >= 45) {
      threatTier = 'HIGH';
    } else if (aggregateScore >= 20) {
      threatTier = 'MODERATE';
    }

    return {
      labels,
      values,
      aggregateScore,
      threatTier,
    };
  }

  /**
   * Generates chart styling parameters based on risk tier.
   */
  public static getRadarVisualStyling(threatTier: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL') {
    switch (threatTier) {
      case 'CRITICAL':
        return {
          backgroundColor: 'rgba(239, 68, 68, 0.25)',
          borderColor: '#ef4444',
          pointBackgroundColor: '#dc2626',
          pointBorderColor: '#ffffff',
        };
      case 'HIGH':
        return {
          backgroundColor: 'rgba(249, 115, 22, 0.25)',
          borderColor: '#f97316',
          pointBackgroundColor: '#ea580c',
          pointBorderColor: '#ffffff',
        };
      case 'MODERATE':
        return {
          backgroundColor: 'rgba(245, 158, 11, 0.25)',
          borderColor: '#f59e0b',
          pointBackgroundColor: '#d97706',
          pointBorderColor: '#ffffff',
        };
      case 'LOW':
      default:
        return {
          backgroundColor: 'rgba(16, 185, 129, 0.25)',
          borderColor: '#10b981',
          pointBackgroundColor: '#059669',
          pointBorderColor: '#ffffff',
        };
    }
  }
}
