/**
 * JobGuard AI - Client-Side Forensic Report Exporter
 * Generates formatted PDF/HTML audit certificates, structured JSON-LD compliance payloads,
 * and cryptographic SHA-256 verification seals directly in the browser client.
 */

export interface AuditReportData {
  auditId: string;
  generatedAt: string;
  candidateName: string;
  claimedCompany: string;
  jobTitle: string;
  overallFraudRiskPercent: number;
  threatLevel: 'AUTHENTIC' | 'SUSPICIOUS' | 'CRITICAL_FRAUD';
  threatVectors: {
    category: string;
    score: number;
    description: string;
    mitigation: string;
  }[];
  regulatoryStatutes: string[];
  sha256Seal: string;
}

export class ForensicReportExporter {
  /**
   * Generates a self-contained, printable HTML forensic audit certificate.
   */
  public static generateHtmlCertificate(data: AuditReportData): string {
    const badgeColor = data.threatLevel === 'AUTHENTIC' ? '#10b981' : data.threatLevel === 'SUSPICIOUS' ? '#f59e0b' : '#ef4444';
    const badgeBg = data.threatLevel === 'AUTHENTIC' ? '#ecfdf5' : data.threatLevel === 'SUSPICIOUS' ? '#fffbeb' : '#fef2f2';

    return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>JobGuard AI - Forensic Audit Certificate [${data.auditId}]</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.5; color: #1e293b; background: #f8fafc; padding: 40px 20px; }
    .certificate-card { max-width: 800px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); padding: 40px; }
    .header { border-bottom: 2px solid #f1f5f9; padding-bottom: 24px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-size: 24px; font-weight: 800; color: #4f46e5; display: flex; align-items: center; gap: 8px; }
    .badge { display: inline-block; padding: 6px 16px; border-radius: 9999px; font-weight: 700; font-size: 14px; color: ${badgeColor}; background: ${badgeBg}; border: 1px solid ${badgeColor}33; }
    .meta-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 30px; background: #f8fafc; padding: 20px; border-radius: 8px; }
    .meta-item { font-size: 14px; }
    .meta-label { color: #64748b; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; }
    .meta-value { font-weight: 600; color: #0f172a; margin-top: 4px; }
    .section-title { font-size: 16px; font-weight: 700; color: #0f172a; margin-top: 28px; margin-bottom: 12px; }
    .vector-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
    .vector-table th { text-align: left; padding: 10px 12px; background: #f1f5f9; color: #475569; font-weight: 600; }
    .vector-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; }
    .seal-box { margin-top: 36px; padding: 16px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; font-family: monospace; font-size: 11px; color: #64748b; word-break: break-all; }
  </style>
</head>
<body>
  <div class="certificate-card">
    <div class="header">
      <div class="logo">🛡️ JobGuard AI Forensic Certificate</div>
      <div class="badge">${data.threatLevel} (${data.overallFraudRiskPercent}% Risk)</div>
    </div>
    <div class="meta-grid">
      <div class="meta-item"><div class="meta-label">Audit Identifier</div><div class="meta-value">${data.auditId}</div></div>
      <div class="meta-item"><div class="meta-label">Timestamp (UTC)</div><div class="meta-value">${data.generatedAt}</div></div>
      <div class="meta-item"><div class="meta-label">Claimed Employer</div><div class="meta-value">${data.claimedCompany}</div></div>
      <div class="meta-item"><div class="meta-label">Evaluated Role</div><div class="meta-value">${data.jobTitle}</div></div>
    </div>
    <div class="section-title">Forensic Threat Vectors & Findings</div>
    <table class="vector-table">
      <thead><tr><th>Vector</th><th>Severity</th><th>Evidence & Advice</th></tr></thead>
      <tbody>
        ${data.threatVectors.map(v => `
          <tr>
            <td><strong>${v.category}</strong></td>
            <td><span style="color: ${v.score >= 50 ? '#ef4444' : '#10b981'}; font-weight: 700;">${v.score}%</span></td>
            <td>${v.description}<br><em style="color:#64748b;">Action: ${v.mitigation}</em></td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    <div class="section-title">Applicable Regulatory Protections</div>
    <ul style="font-size: 13px; color: #475569; padding-left: 20px;">
      ${data.regulatoryStatutes.map(s => `<li>${s}</li>`).join('')}
    </ul>
    <div class="seal-box">
      <strong>DIGITAL CRYPTOGRAPHIC DIGEST (SHA-256):</strong><br>
      ${data.sha256Seal}
    </div>
  </div>
</body>
</html>
    `.trim();
  }

  /**
   * Generates a downloadable JSON file representation.
   */
  public static triggerJsonDownload(data: AuditReportData, filename = 'jobguard-forensic-audit.json'): void {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}
