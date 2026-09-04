/**
 * JobGuard AI - Candidate Safety Advisory Client Engine
 * Provides interactive candidate advisory dialogues, immediate risk containment suggestions,
 * and automated polite counter-response drafts to suspicious recruiter requests.
 */

export interface AdvisoryContext {
  overallRiskScore: number;
  detectedThreatFlags: string[];
  recruiterChannel: 'EMAIL' | 'TELEGRAM' | 'WHATSAPP' | 'SMS' | 'LINKEDIN';
  demandedItems: ('MONEY' | 'CHECK_DEPOSIT' | 'SSN' | 'BANK_LOGIN' | 'PHOTO_ID')[];
}

export interface CandidateGuidance {
  headline: string;
  safetyCalloutType: 'DANGER' | 'WARNING' | 'SAFE';
  keyDirectives: string[];
  suggestedRecruiterReply: string;
  reportingAuthorityLink: string;
}

export class CandidateSafetyAdvisor {
  /**
   * Generates real-time contextual guidance for job seekers.
   */
  public static synthesizeGuidance(ctx: AdvisoryContext): CandidateGuidance {
    const isCritical = ctx.overallRiskScore >= 60 || ctx.demandedItems.includes('MONEY') || ctx.demandedItems.includes('CHECK_DEPOSIT');

    if (isCritical) {
      return {
        headline: '🚨 Critical Scam Warning: Cease Communication Immediately',
        safetyCalloutType: 'DANGER',
        keyDirectives: [
          'Do NOT send any money, cryptocurrency, or gift cards under any circumstances.',
          'Do NOT deposit any check sent to you in the mail or via email.',
          'Do NOT share your Social Security Number, banking passwords, or identity documents.',
          'Block this recruiter on messaging channels and report the listing to JobGuard and IC3.gov.',
        ],
        suggestedRecruiterReply:
          'Due to security policy, I cannot accept third-party check disbursements or pay upfront onboarding fees. Please provide an official application link on your company’s verified website.',
        reportingAuthorityLink: 'https://www.ic3.gov/',
      };
    }

    if (ctx.overallRiskScore >= 30 || ctx.recruiterChannel === 'TELEGRAM' || ctx.recruiterChannel === 'WHATSAPP') {
      return {
        headline: '⚠️ Caution: Unverified Recruitment Channel Detected',
        safetyCalloutType: 'WARNING',
        keyDirectives: [
          'Request a formal video interview with cameras turned on before advancing.',
          'Verify that the recruiter is emailing from an official corporate domain (@company.com).',
          'Cross-reference this job opening directly on the official employer careers portal.',
        ],
        suggestedRecruiterReply:
          'Thank you for reaching out. Before completing additional questionnaires, I would appreciate scheduling a brief live video meeting or phone call with the hiring manager.',
        reportingAuthorityLink: 'https://reportfraud.ftc.gov/',
      };
    }

    return {
      headline: '✅ Standard Precautions: Opportunity Appears Authentic',
      safetyCalloutType: 'SAFE',
      keyDirectives: [
        'Maintain standard personal data privacy during the interview process.',
        'Ensure all offer letters and salary details are documented in a formal written contract.',
      ],
      suggestedRecruiterReply: 'Thank you for the update. I look forward to the next steps in the interview process.',
      reportingAuthorityLink: 'https://www.ftc.gov/',
    };
  }
}
