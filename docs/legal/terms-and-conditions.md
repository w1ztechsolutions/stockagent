# Terms and Conditions

**Last Updated:** 26 October 2026  
**Effective Date:** 26 October 2026  
**Jurisdiction:** Republic of Malawi

---

## 1. Acceptance

By accessing or using the Phungu Insights service (the "Service"), including the public analytics portal at `mse-portal.wiztechsol-info.workers.dev`, the local FastAPI Agent application, and any associated documentation or tools, you ("User", "you") agree to be bound by these Terms and Conditions. If you do not agree to these Terms, you must not use the Service.

These Terms are governed by and construed in accordance with the laws of the **Republic of Malawi**, including the **Companies Act (No. 15 of 2013)**, the **Data Protection Act, 2024**, and the **Constitution of the Republic of Malawi**.

## 2. Description of Service

Phungu Insights provides:

1. **Public Analytics Portal** — A website serving market data, indices, model verdicts, portfolio optimization tools, and educational content for the Malawi Stock Exchange (MSE)
2. **Local Agent Application** — A standalone FastAPI-based AI assistant for MSE query and validation (runs on `127.0.0.1`)
3. **Documentation and Tools** — Reference materials, API documentation, and analytical tools

The Service is provided **"as is"** and on an **"as available"** basis only, without warranties of any kind, either express or implied.

## 3. Data Sources and Accuracy

### 3.1 Market Data Source

Market data is sourced from the **Malawi Stock Exchange** (mse.co.mw) and is used in accordance with the Exchange's terms of use:

- Access to and use of MSE data is **for personal and non-commercial use only**
- Data is provided "as is" without guarantee of accuracy, timeliness, or completeness
- MSE reserves the right to make changes to data at any time without prior notice

### 3.2 No Warranty of Accuracy

While we take reasonable steps to ensure the accuracy of Market Data:

- Market data is sourced from public PDFs published by the MSE
- Data may contain source errors, typos, or gaps
- We apply validation and verification procedures (see `docs/PROJECT.md` §6.2), but we **do not warrant** that all data is free from errors
- **You bear the responsibility** to verify any data you rely upon for decision-making

### 3.3 Data Freshness

- Market data on the public portal is updated via scheduled ETL workflows (weekdays at 09:00, 13:00, 15:30 CAT)
- Live prices on the MSE website update every 5 minutes during trading hours
- Stale data may be displayed outside trading hours

## 4. User Conduct

When using the Service, you agree:

4.1 Not to use the Service for any illegal purpose under Malawian law  
4.2 Not to attempt to gain unauthorized access to any systems or data  
4.3 Not to reproduce, distribute, or exploit any content except as permitted by law  
4.4 Not to use any automated system (scraping bots, etc.) to access the Service  
4.5 To comply with all applicable laws, including the **Data Protection Act, 2024**

## 5. Non-Commercial Use

**5.1 Personal Use Only.** The Service is intended for personal, non-commercial use by individuals interested in Malawi Stock Exchange data.

**5.2 Commercial Use.** Commercial entities, financial advisors, or institutional users must seek explicit permission and may be required to enter into a separate data licensing agreement with the Malawi Stock Exchange.

**5.3 Redistribution Prohibited.** Any redistribution of market data for commercial purposes is prohibited without prior written consent from the Malawi Stock Exchange and Phungu Insights.

## 6. Third-Party Services

### 6.1 Provider Services

The Local Agent uses third-party language model providers:

| Provider | Purpose | Terms |
|----------|---------|-------|
| Ollama | Local model inference | https://ollama.com/terms |
| OpenRouter | API-based LLM access | https://openrouter.ai/terms |
| Google Gemini | API-based LLM access | https://ai.google.dev/terms |
| Groq | API-based LLM access | https://groq.com/terms |

Your interactions with these providers are governed by their respective terms.

### 6.2 Data Provider

Market data is sourced from the Malawi Stock Exchange (mse.co.mw). Their terms can be found at their website.

### 6.3 No endorsement

The Service is not affiliated with, endorsed by, or connected to the Malawi Stock Exchange, the Reserve Bank of Malawi, or any broker, bank, or financial institution.

## 7. Intellectual Property

### 7.1 Phungu Insights Content

All intellectual property rights in the Service software, documentation, branding, and original content (excluding sourced market data) are owned by or licensed to Phungu Insights.

### 7.2 Open Source

The project is distributed under the MIT License. See `LICENSE` in the repository root for details.

### 7.3 Third-Party Marks

The "Phungu Insights" name and logo are marks of Phungu Insights. The Malawi Stock Exchange name and logo are marks of the Malawi Stock Exchange. All other marks are the property of their respective owners.

## 8. Limitation of Liability

**Under Malawian law**, to the maximum extent permitted by law:

### 8.1 No Investment Advice

The Service provides **informational purposes only**. Nothing constitutes investment advice, a recommendation to buy or sell securities, or a solicitation of any investment. Trading involves risk and you may lose money.

### 8.2 Data Accuracy

Phungu Insights shall not be liable for any:

- Errors, omissions, or inaccuracies in market data
- Delays or interruptions in data availability
- Decisions made based on information provided by the Service
- Damages (direct, indirect, incidental, consequential, or punitive) arising from use of the Service

### 8.3 Local Agent Liability

The Local Agent is provided "as is" without warranty of any kind. The Agent's AI-generated responses may contain errors, hallucinations, or inaccuracies. You should always verify information independently.

## 9. Indemnification

You agree to indemnify, defend, and hold harmless Phungu Insights, its developers, and affiliates from and against any claims, liabilities, damages, losses, or expenses (including reasonable legal fees) arising out of your breach of these Terms or your violation of any law.

## 10. Governing Law and Dispute Resolution

These Terms are governed by and construed in accordance with the laws of **Malawi**. Any dispute, controversy, or claim arising out of or in connection with these Terms, including any question regarding its existence, validity, interpretation, performance, breach, or termination, shall be subject to the exclusive jurisdiction of the **courts of Malawi**.

## 11. Changes to Terms

We may update these Terms from time to time. The "Last Updated" date at the top will reflect changes. Your continued use of the Service after changes constitutes acceptance of the revised Terms.

## 12. Severability

If any provision of these Terms is held to be invalid or unenforceable, the remaining provisions will remain in full force and effect.

## 13. Entire Agreement

These Terms, together with the Privacy Policy, Data Usage Declaration, AI Agents Disclaimer, and any additional legal documents in `docs/legal/`, constitute the entire agreement between you and Phungu Insights regarding the Service.

## 14. Contact

For questions about these Terms and Conditions, contact:

- **Project Contact:** See `AGENT.md` at the repository root
- **Email:** See project documentation for current contact
- **Postal:** Phungu Insights, c/o Developer, Blantyre, Malawi

---

*These Terms do not exclude or limit any liability that cannot be excluded or limited under applicable Malawian law.*