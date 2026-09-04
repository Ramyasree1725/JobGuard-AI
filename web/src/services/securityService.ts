/**
 * JobGuard Web Architecture - Client-Side Cryptographic & Security Service
 * Implements client-side SHA-256 hashing, PII masking, and local storage encryption.
 */

export class SecurityService {
  /**
   * Compute WebCrypto SHA-256 digest
   */
  public static async hashText(text: string): Promise<string> {
    if (!text) return '';
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
  }

  /**
   * Redact sensitive personal data before transmitting to AI services
   */
  public static scrubPII(rawText: string): string {
    return rawText
      .replace(/\b\d{3}[- ]?\d{2}[- ]?\d{4}\b/g, '[REDACTED_SSN]')
      .replace(/\b[2-9]\d{3}[- ]?\d{4}[- ]?\d{4}\b/g, '[REDACTED_AADHAAR]')
      .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/g, '[REDACTED_EMAIL]')
      .replace(/\b(?:\+?\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b/g, '[REDACTED_PHONE]');
  }

  /**
   * Validate recruiter email domain against free public webmail list
   */
  public static isFreeWebmail(email: string): boolean {
    const freeDomains = [
      'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
      'aol.com', 'protonmail.com', 'yandex.com', 'mail.com', 'zoho.com'
    ];
    if (!email || !email.includes('@')) return false;
    const domain = email.split('@')[1].trim().toLowerCase();
    return freeDomains.includes(domain);
  }
}
