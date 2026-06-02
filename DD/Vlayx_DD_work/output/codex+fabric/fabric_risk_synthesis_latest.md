## Vlayx Due Diligence Risk Synthesis

**Assessment basis:** Review summary from extracted diligence artifacts: **582 original tree files inventoried recursively**, **135 ZIP-expanded files reviewed**, **717 manifest items total**, and **0 extraction errors**.

**Important limitation:** This synthesis is based only on the provided corpus summary. All findings in the final diligence deck should remain explicitly tied to the relevant source files or extracted artifacts. No unsupported claims should be included.

---

## Preliminary Risk Rating: **High**

Vlayx should be treated as **High Risk pending follow-up and remediation** due to a combination of financial diligence concerns, credential exposure, revenue concentration, incomplete pipeline support, and security evidence gaps.

The rating may be reduced if Vlayx provides satisfactory explanations, corrected financial materials, evidence of credential rotation and control improvements, receivables support, customer concentration analysis, and sufficient security/privacy documentation.

---

## Key Risk Drivers

### 1. Financial Presentation and Reporting Concerns

The diligence corpus indicates a **FY26 books/provisional income and cash presentation mismatch**.

This is a material diligence concern because inconsistent financial presentation may affect confidence in:

- Revenue and income reporting;
- Cash position and liquidity;
- Management reporting reliability;
- Forecast and runway assumptions;
- Investor, customer, or acquirer reliance on financial materials.

#### Follow-ups

Vlayx should provide:

1. A reconciliation between FY26 books, provisional income, and cash presentation.
2. Management explanation for the mismatch.
3. Bank statements supporting cash balances.
4. Trial balance, general ledger, and management accounts for the affected period.
5. Confirmation whether the mismatch is timing-related, classification-related, or an error.
6. Updated financials, if corrections are required.

---

### 2. Plaintext Tax and Compliance Credentials

The corpus summary identifies **plaintext Professional Tax, GST, Income Tax, and TRACES credentials**.

This is a significant security and compliance concern. Plaintext credential storage creates risk of unauthorized access to sensitive government/tax portals, potential alteration or exfiltration of compliance records, and broader account compromise if credentials are reused.

#### Risk implications

- Unauthorized access to tax and statutory accounts;
- Exposure of regulated financial/compliance information;
- Weak credential management practices;
- Potential breach notification or regulatory implications depending on access and exposure;
- Possible indication of broader secrets-management gaps.

#### Follow-ups

Vlayx should provide:

1. Confirmation that all exposed credentials have been rotated.
2. Date/time of rotation and list of affected accounts.
3. Evidence that plaintext credentials have been removed from repositories, documents, shared drives, and backups where feasible.
4. Explanation of how the credentials became stored in plaintext.
5. Current secrets management process.
6. Access control list for users with access to tax/compliance credentials.
7. Whether multi-factor authentication is enabled for GST, Income Tax, TRACES, and Professional Tax portals where supported.
8. Incident review or internal assessment confirming whether unauthorized access occurred.

---

### 3. Revenue Concentration in Shopsense/Fynd

The review indicates **revenue invoice concentration in Shopsense/Fynd**.

Customer or platform concentration may materially affect business resilience. If revenue is heavily dependent on one counterparty, platform, or related business channel, Vlayx may face increased commercial risk if that relationship changes.

#### Risk implications

- Dependency on one major customer or platform;
- Potential revenue volatility;
- Contract renewal or termination risk;
- Lower diversification of revenue base;
- Reduced reliability of revenue forecasts if pipeline is not independently supported.

#### Follow-ups

Vlayx should provide:

1. Customer-level revenue breakdown by month and fiscal year.
2. Percentage of revenue attributable to Shopsense/Fynd.
3. Copies of governing agreements, purchase orders, SOWs, or invoices supporting that revenue.
4. Contract term, renewal rights, termination rights, and payment terms.
5. Aging and collection history for invoices tied to Shopsense/Fynd.
6. Explanation of whether Shopsense/Fynd is a customer, partner, platform, affiliate, or related party.
7. Revenue forecast with and without Shopsense/Fynd contribution.

---

### 4. Accounts Receivable Aging Includes Old Receivables

The corpus summary notes that **AR aging includes old receivables**.

Aged receivables may indicate collectability issues, revenue recognition concerns, customer disputes, or cash flow risk.

#### Risk implications

- Potential overstatement of assets;
- Possible bad debt exposure;
- Weak collections process;
- Revenue recognition concerns if invoices are not collectible;
- Cash flow and working capital pressure.

#### Follow-ups

Vlayx should provide:

1. Full AR aging report by customer and invoice.
2. Supporting invoices and payment status for older receivables.
3. Subsequent collections evidence after the reporting date.
4. Management assessment of collectability.
5. Bad debt reserve policy.
6. Identification of disputed, written-off, or impaired receivables.
7. Reconciliation of AR aging to the general ledger.

---

### 5. Pipeline Evidence Incomplete

The diligence summary states that **pipeline evidence is incomplete**.

Incomplete pipeline support limits confidence in forward-looking revenue claims, growth assumptions, and valuation support.

#### Risk implications

- Forecast may not be substantiated;
- Pipeline may include uncommitted or speculative opportunities;
- Risk of overstated growth expectations;
- Difficulty validating sales conversion assumptions.

#### Follow-ups

Vlayx should provide:

1. Current pipeline report with opportunity stage, value, probability, expected close date, and owner.
2. Evidence for material pipeline items, such as emails, LOIs, proposals, purchase orders, or draft agreements.
3. Historical conversion rates by stage.
4. Definitions for each pipeline stage.
5. Exclusions for stale, inactive, or duplicate opportunities.
6. Forecast model tying pipeline to projected revenue.

---

### 6. Security Evidence Gaps

The diligence summary identifies **security evidence gaps**.

Because security documentation appears incomplete, the current assessment cannot confirm whether Vlayx has adequate controls for access management, data protection, incident response, secure development, vendor management, or compliance.

#### Risk implications

- Unknown maturity of information security program;
- Potential inadequate access controls;
- Potential lack of incident response readiness;
- Potential lack of vulnerability management;
- Inability to validate claims regarding security posture;
- Increased third-party risk if Vlayx processes sensitive customer, employee, financial, or regulated data.

#### Follow-ups

Vlayx should provide:

1. Information security policy.
2. Access control policy.
3. Password and MFA policy.
4. Incident response plan.
5. Data classification and handling policy.
6. Vulnerability management process.
7. Secure software development lifecycle documentation, if applicable.
8. Penetration test or vulnerability assessment reports, if available.
9. Cloud infrastructure security documentation, if applicable.
10. Data retention and deletion policy.
11. Privacy policy and data processing terms, if personal data is processed.
12. Evidence of employee security training.
13. List of subprocessors or key third-party service providers.
14. Business continuity and disaster recovery documentation.

---

## Recommended Diligence Actions Before Proceeding

Before approving, investing in, acquiring, or onboarding Vlayx, the following actions are recommended:

1. **Source-map every finding** to specific files in the extracted corpus and cite those files in the diligence deck.
2. **Request financial reconciliations** for FY26 income, books, cash, AR, and revenue.
3. **Require credential remediation evidence**, including rotation and implementation of secure secrets management.
4. **Validate revenue concentration** and obtain customer-level revenue support.
5. **Confirm collectability of aged receivables** through subsequent payment evidence or reserve analysis.
6. **Substantiate pipeline claims** with documentary evidence.
7. **Conduct a security questionnaire review** and request supporting policies and technical evidence.
8. **Escalate unresolved material issues** to legal, finance, security, and executive stakeholders before reliance on the diligence package.

---

## Suggested Risk Conditions / Controls

If engagement proceeds before all diligence items are resolved, the following controls should be considered:

1. **No reliance on unsupported financial or pipeline claims** until reconciled and source-backed.
2. **Credential remediation as a condition precedent**, including rotation of exposed government/tax portal credentials.
3. **Restricted data sharing** until Vlayx’s security posture is validated.
4. **Contractual security obligations**, including incident notification, confidentiality, access controls, audit rights, and data deletion.
5. **Enhanced monitoring** for financial reporting updates and customer concentration changes.
6. **Management certification** that all diligence responses are accurate and complete.
7. **Holdback, indemnity, or escrow mechanisms**, if this diligence is tied to investment or acquisition activity.
8. **Periodic security and compliance reviews** if Vlayx is onboarded as a vendor.

---

## Conclusion

Based on the provided diligence corpus summary, Vlayx presents a **High preliminary risk** due to multiple unresolved issues across finance, credential security, revenue concentration, receivables quality, pipeline substantiation, and security evidence.

This rating should be revisited after Vlayx provides source-backed explanations, remediation evidence, reconciliations, and complete security documentation. All final findings should remain tied to specific source files in the diligence deck.
