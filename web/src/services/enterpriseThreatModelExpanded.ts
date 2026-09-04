/**
 * JobGuard AI - Enterprise Threat Model Expanded
 * Client-side threat modeling framework computing STRIDE threat classifications,
 * attack tree paths, and mitigation effectiveness matrices for web applications.
 */

export interface ThreatTreeLeaf {
  leafId: string;
  threatName: string;
  strideCategory: 'SPOOFING' | 'TAMPERING' | 'REPUDIATION' | 'INFORMATION_DISCLOSURE' | 'DENIAL_OF_SERVICE' | 'ELEVATION_OF_PRIVILEGE';
  likelihoodScore: number; // 1 to 5
  impactScore: number; // 1 to 5
  calculatedRiskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  primaryMitigation: string;
}

export class EnterpriseThreatModelExpanded {
  private threatLeaves: ThreatTreeLeaf[] = [];

  constructor() {
    this.initializeThreatModel();
  }

  private initializeThreatModel(): void {
    this.threatLeaves = [
      {
        leafId: 'THR-001',
        threatName: 'Corporate Recruiter Email Domain Spoofing',
        strideCategory: 'SPOOFING',
        likelihoodScore: 5,
        impactScore: 4,
        calculatedRiskLevel: 'CRITICAL',
        primaryMitigation: 'Enforce strict DMARC (p=reject) and DNS SPF alignment checks on all incoming messages.',
      },
      {
        leafId: 'THR-002',
        threatName: 'Counterfeit Employment Check Overpayment Trap',
        strideCategory: 'TAMPERING',
        likelihoodScore: 5,
        impactScore: 5,
        calculatedRiskLevel: 'CRITICAL',
        primaryMitigation: 'Heuristic keyword parsing and immediate candidate banking alert banner notifications.',
      },
      {
        leafId: 'THR-003',
        threatName: 'Premature Candidate SSN and Banking Extraction',
        strideCategory: 'INFORMATION_DISCLOSURE',
        likelihoodScore: 4,
        impactScore: 5,
        calculatedRiskLevel: 'CRITICAL',
        primaryMitigation: 'Zero-knowledge client-side encryption and strict form endpoint verification.',
      },
      {
        leafId: 'THR-004',
        threatName: 'Telegram / WhatsApp Chat Evaluation Channel Redirect',
        strideCategory: 'SPOOFING',
        likelihoodScore: 5,
        impactScore: 3,
        calculatedRiskLevel: 'HIGH',
        primaryMitigation: 'Enforce mandatory live video interview checklist before signing offer documents.',
      },
    ];
  }

  public getThreatsByCategory(category: ThreatTreeLeaf['strideCategory']): ThreatTreeLeaf[] {
    return this.threatLeaves.filter(t => t.strideCategory === category);
  }

  public getHighRiskThreats(): ThreatTreeLeaf[] {
    return this.threatLeaves.filter(t => t.calculatedRiskLevel === 'CRITICAL' || t.calculatedRiskLevel === 'HIGH');
  }
}
