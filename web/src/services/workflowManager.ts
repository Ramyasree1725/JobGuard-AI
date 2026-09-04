/**
 * JobGuard Web Architecture - Application Workflow & Verification Pipeline State
 * Manages reactive scan states, batch execution queues, and complaint generation.
 */

export interface VerificationJob {
  id: string;
  title: string;
  company: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  riskScore: number;
  verdict: string;
  timestamp: string;
}

export class WorkflowManager {
  private static STORAGE_KEY = 'jobguard_web_audit_jobs';

  public static getSavedJobs(): VerificationJob[] {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  public static saveJob(job: VerificationJob): void {
    const list = this.getSavedJobs();
    list.unshift(job);
    const trimmed = list.slice(0, 50); // Keep last 50
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(trimmed));
  }

  public static clearHistory(): void {
    localStorage.removeItem(this.STORAGE_KEY);
  }
}
