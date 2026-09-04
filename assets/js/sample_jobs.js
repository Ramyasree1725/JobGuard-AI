/**
 * JobGuard AI - Rich Sample Datasets for Instant Testing
 * Includes real-world job postings & notorious scam archetypes.
 */

const SAMPLE_JOBS = [
    {
        id: 'scam_telegram_data_entry',
        type: 'scam',
        name: '🚨 Telegram Online Data Entry Scam',
        company: 'Apex Global Logistics LLC',
        title: 'Remote Data Entry Clerk / Assistant',
        salary: '$45 - $65 per hour',
        email: 'apexlogistics.hiring@gmail.com',
        website: 'http://apex-global-careers.info',
        description: `URGENT HIRING! We are looking for immediate remote Data Entry Clerks to join our expanding team. 

Responsibilities:
- Re-type scanned Word and PDF documents
- Simple copy paste tasks from home
- 2 to 3 hours per day

Requirements:
- No experience needed, any age, students and housewives welcome
- Basic computer knowledge
- Immediate start today! Only 3 slots available

Compensation:
- $45 - $65 per hour ($1,800 weekly guaranteed payout)

How to Apply:
Do NOT apply through job boards. Send your resume and contact us directly on Telegram @HiringManager_David for immediate selection without interview. You will receive a cashier check for $2,500 to purchase your home office Apple MacBook and software from our approved vendor. Kindly reply immediately.`
    },
    {
        id: 'scam_crypto_task_rating',
        type: 'scam',
        name: '🚨 Crypto VIP Task / App Rating Scam',
        company: 'Digital Nexus Media',
        title: 'VIP Product & App Reviewer',
        salary: '₹5,000 - ₹12,000 daily',
        email: 'hr.digitalnexus@yahoo.com',
        website: 'http://digital-nexus-vip.cc',
        description: `Part-time work from home opportunity! Earn high commission by rating 5-star reviews on mobile apps and e-commerce products.

Requirements:
- Only need a smartphone and 30 minutes free time daily
- Earn ₹5,000 to ₹12,000 daily payout via UPI or USDT Crypto Wallet

Onboarding Instructions:
- Connect with our team on WhatsApp: +91 98765 43210
- Initial registration fee of ₹1,500 required for account activation and security deposit (100% refundable after 5 tasks).
- Limited slots available! Act now to secure guaranteed job placement.`
    },
    {
        id: 'scam_package_reshipping',
        type: 'scam',
        name: '🚨 Package Reshipping / Mule Scam',
        company: 'Federal Parcel Forwarding',
        title: 'Quality Control Inspector & Package Dispatcher',
        salary: '$3,800 per month + bonuses',
        email: 'careers@fedex-parcel-logistics-corp.com',
        website: 'http://fedex-parcel-logistics-corp.com',
        description: `Inspect high-value luxury goods and forward parcels directly from your home address.

Job Duties:
- Receive packages delivered to your home
- Open and inspect contents (electronics, designer jewelry)
- Re-box and print shipping labels to forward to international addresses

Requirements:
- Valid US address
- Routing number and bank account details required before first day for direct wire transfers
- No prior experience required

Equipment:
- We will mail you a certified cashier's check of $3,200 to purchase shipping supplies and packaging scales from our authorized supplier.`
    },
    {
        id: 'real_google_swe',
        type: 'real',
        name: '✅ Google - Senior Software Engineer',
        company: 'Google LLC',
        title: 'Senior Software Engineer, Cloud Infrastructure',
        salary: '$180,000 - $240,000 / year + equity',
        email: 'recruiting-team@google.com',
        website: 'https://careers.google.com',
        description: `Google's software engineers develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another.

Minimum Qualifications:
- Bachelor's degree in Computer Science, related technical field, or equivalent practical experience.
- 5+ years of experience with software development in Go, C++, Java, or Python.
- Experience with distributed systems, microservices, and large-scale cloud architecture.

Preferred Qualifications:
- Master's degree or PhD in Computer Science or related field.
- Experience with Kubernetes, gRPC, and high-throughput low-latency telemetry pipelines.

Responsibilities:
- Design, develop, test, deploy, maintain, and enhance large-scale distributed cloud systems.
- Collaborate with cross-functional engineering and product management teams.

Benefits:
- Comprehensive medical, dental, and vision health insurance
- 401(k) matching program, Paid Time Off (PTO), parental leave, and wellness stipends.
- Equal Opportunity Employer (EOE).

Please apply directly via our careers page at greenhouse.io or careers.google.com. Google will never ask for payment or banking information during the recruitment process.`
    },
    {
        id: 'real_microsoft_analyst',
        type: 'real',
        name: '✅ Microsoft - Data & Business Analyst',
        company: 'Microsoft Corporation',
        title: 'Data & Business Intelligence Analyst',
        salary: '$110,000 - $145,000 / year',
        email: 'talent@microsoft.com',
        website: 'https://careers.microsoft.com',
        description: `At Microsoft, our mission is to empower every person and every organization on the planet to achieve more.

Qualifications:
- Bachelor's degree in Statistics, Business Analytics, Computer Science, or equivalent experience.
- 3+ years of experience with SQL, Power BI, Python, and data modeling.
- Strong communication and stakeholder presentation skills.

Key Responsibilities:
- Build executive dashboards, automate ETL pipelines, and interpret customer engagement metrics.
- Collaborate with cross-functional product teams to drive data-informed decisions.

Equal opportunity employer committed to a diverse and inclusive workplace. Comprehensive 401(k), health coverage, and employee stock purchase plan provided. Apply via Microsoft Careers Portal.`
    }
];

const SAMPLE_OFFER_LETTERS = [
    {
        id: 'offer_fake_check',
        name: '🚨 Fake Check Equipment Scam Offer Letter',
        text: `OFFICIAL EMPLOYMENT OFFER & APPOINTMENT LETTER
Company: Global Tech Horizon Inc.

Dear Candidate,

Following your evaluation, we are thrilled to offer you the position of Remote Administrative Assistant. Your starting compensation will be $52.00 per hour.

IMPORTANT ONBOARDING CLAUSE:
To prepare your home workstation, our finance department has enclosed a cashier's check in the amount of $4,850.00. You are strictly instructed to deposit the check into your personal bank account. Once funds appear available, wire $4,200 via Zelle or Western Union to our certified IT equipment vendor (Apex Supplies) within 24 hours to expedite your Apple MacBook Pro and dual monitor setup.

Please provide your complete online banking credentials and Social Security Number for direct payroll setup before your start date. Immediate acceptance required within 12 hours or this offer will be forfeited.`
    },
    {
        id: 'offer_legit_corporate',
        name: '✅ Legitimate Enterprise Offer Letter',
        text: `CONFIDENTIAL EMPLOYMENT OFFER LETTER
Company: Stripe, Inc.
Position: Frontend Systems Engineer

Dear Candidate,

We are excited to extend an offer of employment for the position of Frontend Systems Engineer at Stripe.

Compensation & Benefits:
- Base Salary: $165,000 USD annualized, paid semi-monthly.
- Equity: Restricted Stock Units (RSUs) valued at $120,000 subject to standard 4-year vesting schedule.
- Health Insurance: Comprehensive medical, dental, and vision insurance with 100% employer-covered premiums.
- Equipment: Corporate laptop and security peripherals will be provisioned and shipped directly to your residence by Stripe IT Operations at zero expense to you.

Conditions of Offer:
This offer is contingent upon successful completion of standard background verification and authorization to work in the United States (I-9 verification). Onboarding documents and direct deposit information will be submitted securely through our internal Workday HR portal on your official start date.

Please review this offer and return the signed agreement by Friday, 5:00 PM PST.`
    }
];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SAMPLE_JOBS, SAMPLE_OFFER_LETTERS };
}
