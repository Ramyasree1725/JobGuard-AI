/**
 * JobGuard Web Architecture - Client Threat Intelligence Service
 * Fast in-browser matching of recruiter phone numbers, Telegram handles, and UPI IDs.
 */

export interface BlacklistHit {
  type: string;
  value: string;
  actor: string;
  riskPenalty: number;
}

export class ThreatIntelligenceService {
  private static knownScamHandles: Map<string, string> = new Map([
    ['@hiringmanager_david', 'Apex Global Impersonator Ring'],
    ['@hr_recruiter_quickhire', 'Task Recharge Syndicate'],
    ['hr.digitalnexus@paytm', 'Task Investment Fraud Network'],
    ['+919876543210', 'WhatsApp Fake Check Syndicate'],
  ]);

  public static checkHandle(query: string): BlacklistHit | null {
    if (!query) return null;
    const clean = query.trim().toLowerCase().replace(/\s+/g, '');
    for (const [handle, actor] of this.knownScamHandles.entries()) {
      if (clean.includes(handle) || handle.includes(clean)) {
        return {
          type: 'blacklisted_entity',
          value: handle,
          actor: actor,
          riskPenalty: 80,
        };
      }
    }
    return null;
  }
}
