# Privacy Policy

**Last Updated:** 26 October 2026  
**Effective Date:** 26 October 2026  
**Jurisdiction:** Republic of Malawi

---

## 1. Introduction

Phungu Insights ("we", "us", "our") operates the Phungu Insights platform (the "Service"), including the public-facing analytics portal at `mse-portal.wiztechsol-info.workers.dev` and the local FastAPI agent application (the "Agent"). This Privacy Policy explains how we collect, use, store, and protect information in accordance with the **Data Protection Act, 2024 (Act No. 3 of 2024)** of Malawi and the **Constitution of the Republic of Malawi, Section 21** (right to privacy).

The Malawi Data Protection Authority (DPA), operating under the Malawi Communications Regulatory Authority (MACRA), is the supervisory authority for this Act. Their contact details are:

- **Data Protection Authority (DPA)**
- 1st Floor, Green Heritage House, 2 Khonje Close, City Centre
- P.O. Box 30214, Lilongwe, Malawi
- Email: info@dpa.mw
- Phone: +265 991 80 21 80
- Website: https://www.dpa.mw

## 2. Information We Collect

### 2.1 Data You Provide to the Agent (Local App)

When you interact with the Agent application running locally:

- **Chat messages** — your questions and conversation history (stored only in your browser tab, not persisted on our servers)
- **Database connection strings** — provided via environment variables to connect to read-only PostgreSQL (Neon)

### 2.2 Data Collected Automatically

- **API requests** — When using the public portal or API endpoints, we may log technical information (IP address, user agent, request timestamps) for security and debugging purposes
- **Usage analytics** — We do not use third-party analytics services by default. Any analytics are self-hosted and anonymized

### 2.3 Data We Do NOT Collect

- **Personal identification data** — The portal operates without user accounts. We do not collect names, email addresses, phone numbers, or other personally identifiable information from general visitors
- **Portfolio or holdings data** — User-specific financial data, if added in future versions, will be stored locally in the browser or in the user's chosen database, not on our servers
- **Device identifiers** — We do not use device fingerprinting or persistent tracking identifiers

## 3. Legal Basis for Processing

Under the Data Protection Act, 2024, we process data on the following lawful bases:

| Basis | Application |
|-------|-------------|
| **Consent** (Section 8) | When you explicitly provide data (e.g., feedback, contact forms) |
| **Legitimate interests** (Section 8(b)) | Security logging, debugging technical issues |
| **Performance of a task carried out in the public interest** (Section 8(c)) | Serving public market data and educational financial information |

For the current read-only portal and local Agent, processing is minimal and primarily consists of temporary session data and read-only database queries.

## 4. What We Do With Your Data

### 4.1 Data Usage Purposes

1. **Provide the service** — Serve market data, answer queries, generate analytics
2. **Security and fraud prevention** — Protect the service from abuse, detect technical issues
3. **Debugging and improvement** — Identify bugs, improve performance (temporary logs only)

### 4.2 What We Do NOT Do

- We do **not** sell, rent, or monetize your data
- We do **not** share your data with third parties for marketing purposes
- We do **not** use your data for automated decision-making or profiling
- We do **not** use real-time AI sentiment inference on personal data

## 5. Data Storage and Retention

### 5.1 Local Agent Data

- Chat history is stored only in your browser session and is cleared on tab reload
- No conversation data is persisted to disk by the application
- Database connection strings are stored in your local environment variables

### 5.2 Server Logs

- Technical logs (IP addresses, request timestamps) are retained for **90 days** maximum
- Logs are stored encrypted and accessed only for security and debugging

### 5.3 Database Data

- Market data is sourced from the Malawi Stock Exchange (see [Data Usage Declaration](./data-usage-declaration.md) for non-commercial use terms)
- All stored data is market data or derived analytics (not personal data)

## 6. Your Rights Under the Data Protection Act, 2024

You have the following rights under Malawian law:

- **Right to be informed** (Section 12) — You are informed about data collection via this policy
- **Right of access** (Section 13) — Request a copy of any data we hold about you
- **Right to rectification** (Section 14) — Correct inaccurate personal data
- **Right to erasure** (Section 15) — Request deletion of your data (where applicable)
- **Right to restrict processing** (Section 16)
- **Right to data portability** (Section 17)
- **Right to object** (Section 18) — Object to processing for marketing or legitimate interests
- **Right to withdraw consent** (Section 8) — At any time, without affecting lawfulness before withdrawal

To exercise any of these rights, contact us at:

- **Email:** privacy@phungu-insights.mw (or the contact provided in AGENT.md)
- **Data Protection Authority:** info@dpa.mw

## 7. Children's Privacy

This Service is **not directed at children under 18**. We do not knowingly collect personal data from children. If we become aware that we have collected data from a child, we will take steps to delete it promptly.

## 8. International Transfers

The Service is hosted within Malawi and the data is stored in servers physically located in Malawi and/or the European Union (via Neon). When data is transferred outside Malawi, we ensure it receives equivalent protection under the Data Protection Act, 2024 (Section 27 — Conditions for transfer).

## 9. Security Measures

We implement appropriate technical and organizational measures in accordance with **Section 19 of the Data Protection Act, 2024**:

- **Encryption in transit** — HTTPS/TLS for all web traffic
- **Database access controls** — Read-only database connections with parameterized queries (no DROP/TRUNCATE/ALTER)
- **SSRF protection** — URL fetch tools validate against private/reserved IP ranges
- **No hardcoded credentials** — All secrets via environment variables
- **Regular updates** — Dependencies updated promptly for security patches

## 10. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. The "Last Updated" date at the top will reflect changes. Major changes will be communicated through the application or via the project's changelog.

## 11. Contact Us

If you have questions about this Privacy Policy or your data rights:

- **Project Contact:** See `AGENT.md` at the repository root for contact information
- **Data Protection Authority:** info@dpa.mw | +265 991 80 21 80
- **Mailing Address:** Data Protection Authority, Green Heritage House, 2 Khonje Close, Lilongwe

## 12. Applicable Law

This Privacy Policy is governed by and construed in accordance with the laws of **Malawi**, including:

- The **Data Protection Act, 2024 (Act No. 3 of 2024)**
- The **Constitution of the Republic of Malawi (Section 21)**
- The **Electronic Transactions and Cybersecurity Act No. 33 of 2016**

---

*This document is provided in English. Where translations exist, the English version prevails.*