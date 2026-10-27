# Data Usage Declaration — Non-Commercial Use of MSE Data

**Last Updated:** 26 October 2026  
**Effective Date:** 26 October 2026  
**Jurisdiction:** Republic of Malawi

---

## 1. Purpose

This Data Usage Declaration clarifies the terms under which market data from the **Malawi Stock Exchange** (mse.co.mw) is collected, processed, stored, and presented by Phungu Insights. This declaration is aligned with the **Malawi Stock Exchange's Terms of Use** and the **Data Protection Act, 2024** of Malawi.

## 2. Malawi Stock Exchange Data Terms

The Malawi Stock Exchange states the following regarding its website and market data:

> "To access the Malawi Stock Exchange website (the 'Website') and its market data (the 'Data'), you must agree to the below notice and disclaimer (the 'Terms'). If you do not agree to the Terms, then you must refrain from using the Website and the Data.
>
> Unless otherwise stated, the Website and Data is the copyright of the Malawi Stock Exchange.
>
> Access to and use of the Website and the Data is for **personal and non-commercial use only**. No part of the Website or Data may be copied, reproduced, republished, downloaded, posted, broadcast or transmitted in any way for any commercial purpose and/or exploited for profit. Those that intend to use the website and data for **commercial purposes** must first notify the Exchange to sign a data agreement.
>
> The Website and Data is provided **'as is'** and on an **'as available'** basis only and no guarantee is made as to the accuracy, timeliness, completeness, or fitness for a particular purpose of the Website or any of the Data. While care has been taken to ensure that all Data provided on the Website is correct at the time of publication, the Malawi Stock Exchange does not accept any responsibility for any errors, omissions, or inaccurate Data on the Website.
>
> The Malawi Stock Exchange reserves the right to make changes to the Website and/or Data at any time without prior notice."

## 3. Data Collection Methodology

Phungu Insights collects market data through the following methodology:

### 3.1 Source

All market data originates from official **Malawi Stock Exchange daily market reports** published as PDF documents on `mse.co.mw`. These include:

- Daily price data (open, high, low, close, volume, turnover)
- Fundamental data (P/E ratio, dividend yield, market capitalization)
- Official index values (MASI, DSI, FSI)
- Corporate announcements
- Market calendar data

### 3.2 Processing

Data is processed through:

1. **PDF Download** — Official market reports fetched from mse.co.mw
2. **Parsing** — Structured extraction using `pdfplumber` and regex patterns
3. **Validation** — Business rule checks (symbol normalization, date validation, price boundary checks, previous-close chain integrity)
4. **Split Adjustments** — Historical price adjustments for corporate actions (e.g., PCL 1:35 split)
5. **Dual-Writing** — Data stored to both Base44 entities and Neon PostgreSQL

### 3.3 Data Fields

The following market data fields are collected:

| Category | Fields |
|----------|--------|
| Price Data | Symbol, Trade Date, Open Price, Close Price, Previous Close, Change Percent, Volume, Turnover |
| Fundamentals | P/E Ratio, Dividend Yield, Market Capitalization, Price-to-Book Value |
| Index Data | MASI, Domestic Index, Foreign Index |
| Metadata | Market Type, Data Source, Raw Close Price |

## 4. Non-Commercial Use Declaration

### 4.1 Current Scope

Phungu Insights operates under a **non-commercial, personal use** model:

- ✅ Personal research and portfolio tracking
- ✅ Educational purposes
- ✅ Self-directed investing analysis
- ✅ Non-commercial sharing of derived insights (with attribution)

### 4.2 Prohibited Commercial Uses

The following uses require a **separate commercial data licensing agreement** with the Malawi Stock Exchange:

- ❌ Distributing market data to third parties for commercial gain
- ❌ Using data in paid applications or services
- ❌ Selling or licensing market data
- ❌ High-frequency trading or algorithmic trading services
- ❌ Market data redistribution feeds
- ❌ Incorporating MSE data into commercial investment products

### 4.3 Commercial Inquiry

Entities seeking to use Phungu Insights data for commercial purposes must:

1. Contact the Malawi Stock Exchange directly to negotiate a data licensing agreement
2. Contact the Phungu Insights project maintainers for commercial use inquiries
3. Independently verify the suitability of any data for commercial use

## 5. Data Storage and Access

### 5.1 Public Portal

- Data is served via Cloudflare Workers
- Read-only access; no modifications possible through the public interface
- Data cached for performance; cache invalidation occurs on new ETL runs

### 5.2 Local Agent

- Data accessed via read-only database connections
- No data is stored persistently on user devices beyond browser session
- Connection strings provided by users via environment variables

## 6. Copyright and Attribution

### 6.1 Data Copyright

All market data sourced from the Malawi Stock Exchange remains the **copyright of the Malawi Stock Exchange**. Phungu Insights provides a value-added service of parsing, validation, and presentation.

### 6.2 Required Attribution

When displaying or sharing MSE-sourced market data, you must include attribution:

> "Data sourced from the Malawi Stock Exchange (mse.co.mw). Provided 'as is' without warranty of accuracy, timeliness, or completeness."

### 6.3 No Commercial Redistribution

Redistribution of this data for commercial purposes without a licensing agreement from the Malawi Stock Exchange is prohibited.

## 7. Data Accuracy and Liability

### 7.1 Source Accuracy

The Malawi Stock Exchange provides data "as is" without warranty. Phungu Insights applies the following validation measures to improve data quality:

- Cross-reference of current close vs previous close chains
- Boundary checks between consecutive trading days
- P/E ratio verification (Market Capitalization ÷ After-Tax Profit)
- Split adjustment verification
- Duplicate detection and removal

### 7.2 Known Data Gaps

The following are documented data characteristics, not errors:

- Missing trading days (exchange reports not published)
- Suspended trading days (zero-price days are skipped)
- Historical backfill gaps (under active completion)
- P/BV values sourced from periodic digests (not daily reports)

## 8. Data Retention

- Market data is retained indefinitely for historical analysis
- Server logs containing technical metadata are retained for 90 days
- User chat history in the Agent is not persisted beyond browser session
- Database backups follow the documented dual-write pattern (Base44 + Neon)

## 9. Changes to Data Usage

Phungu Insights reserves the right to modify how data is collected, processed, and stored, provided such changes remain within the bounds of:

- Malawi Stock Exchange Terms of Use
- Data Protection Act, 2024
- Non-commercial use principles

### 9.1 Commercial Licensing

Should Phungu Insights obtain commercial data licensing rights from the Malawi Stock Exchange, users will be separately notified and offered the option to accept updated terms.

## 10. Acknowledgment

By using Phungu Insights, you acknowledge that:

1. You have read and understood the Malawi Stock Exchange's Terms of Use
2. You accept the data is provided "as is" with no warranty of accuracy
3. You will not redistribute or commercially exploit the data without proper licensing
4. You will attribute the Malawi Stock Exchange as the original data source
5. You understand that data may contain errors despite validation efforts

## 11. Contact for Data Licensing

For inquiries about commercial use of MSE data:

- **Malawi Stock Exchange:** See https://mse.co.mw for contact information
- **Phungu Insights:** See `AGENT.md` at the repository root for project contact information

---

*This Data Usage Declaration is maintained by the Phungu Insights project and reflects the status as of the "Last Updated" date. It does not constitute legal advice. For specific legal questions, consult a qualified attorney in Malawi.*