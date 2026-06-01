#!/usr/bin/env python3
from pathlib import Path
import csv
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUT = Path("/Users/basethesis/Desktop/benchmark_hermes-fabric/DD/Vlayx_DD_work/output")
PPTX = OUT / "Vlayx_Due_Diligence_Report.pptx"

sources = {
    "S0": "DD/Vlayx_DD_work/output/manifest.csv and coverage.csv",
    "S1": "Client Inputs/1. Valyx FDD Input/General/FY 2024-25/VWPL_ FR 31.3.2025 - Actuals.xlsx",
    "S2": "Client Inputs/1. Valyx FDD Input/General/YTD/VWPL_ PROVISIONAL FR 28.2.2026 - Actuals.xlsx",
    "S3": "Client Inputs/2. Books Extracts/Profit and Loss - Valyx FDD.xlsx",
    "S4": "Client Inputs/2. Books Extracts/Profit and Loss till YTD Feb-26.xlsx",
    "S5": "Client Inputs/2. Books Extracts/Balance Sheet FY 2024-25.xlsx",
    "S6": "Client Inputs/2. Books Extracts/Balance Sheet YTD Feb-26.xlsx",
    "S7": "Client Inputs/1. Valyx FDD Input/Assets/Trade Receivables/DD8.7 Aging of AR/Aging of Accounts Receivables - 28.2.2026 - Actuals.pdf",
    "S8": "Client Inputs/1. Valyx FDD Input/Assets/Trade Receivables/DD8.7 Aging of AR/AR Aging Details By Invoice Due Date.pdf",
    "S9": "Client Inputs/1. Valyx FDD Input/FDD_Customer_Invoices/*.pdf and duplicate invoice folder",
    "S10": "Client Inputs/1. Valyx FDD Input/KPIs/MIS_RevenueProjection_Customers_Pipeline_Comparables.xlsx",
    "S11": "Client Inputs/21st_April_2026 Valyx Docs/Metrics_till_Mar2026.csv",
    "S12": "Client Inputs/21st_April_2026 Valyx Docs/Pricing Proposal.xlsx",
    "S13": "Client Inputs/21st_April_2026 Valyx Docs/Valyx __ Automation Tracker.xlsx",
    "S14": "Client Inputs/21st_April_2026 Valyx Docs/Mooving_Valyx_Agreement_928b981f-9535-4fe1-818b-a7388d1a4d89.pdf",
    "S15": "Client Inputs/3. Hindware Data Request/Awfis_valyx_agreement-.pdf",
    "S16": "Client Inputs/3. Hindware Data Request/Valyx - AI Powered Billing for AGI Hindware - Scope.pdf",
    "S17": "Client Inputs/1. Valyx FDD Input/Organizationand structure/Org Chart Updated.pptx",
    "S18": "Client Inputs/PreSeedDiligenceProofs/CP Proofs/Valyx - Founder Employment Agreement - Anirudh/Avishek.pdf",
    "S19": "Client Inputs/PreSeedDiligenceProofs/CP Proofs/Executed Version - Valyx - Waveform SSHA (August 28 2023).pdf",
    "S20": "Client Inputs/21st_April_2026 Valyx Docs/Startup Certificate.pdf",
    "S21": "Client Inputs/21st_April_2026 Valyx Docs/Valyx_Mobile device Policy.docx.pdf",
    "S22": "Client Inputs/1. Valyx FDD Input/Login Credentials of Valyx.docx",
    "S23": "Client Inputs/1. Valyx FDD Input/Assets/BS - Liabilities/Trade Payable List along with MSME vendors.xlsx",
    "S24": "Client Inputs/1. Valyx FDD Input/Fixed Deposits/*.txt; FD balance confirmation images",
    "S25": "Client Inputs/3. Hindware Data Request/Valyx Valuation report.pdf; MIS cap table sheet",
}


def add_textbox(slide, x, y, w, h, text, size=13, bold=False, color=(40, 46, 58), align=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = RGBColor(*color)
    if align:
        p.alignment = align
    return box


def add_footer(slide, source_ids):
    # Keep footers legible; full source-file paths are provided in Source Register slides
    # and source_register.csv. Deduplicate while preserving order.
    ids = list(dict.fromkeys(source_ids))
    txt = "Sources: " + ", ".join(ids) + " (see Source Register slides / source_register.csv for file paths)"
    add_textbox(slide, 0.45, 7.05, 12.4, 0.32, txt, size=7, color=(95, 103, 115))


def add_title(slide, title, subtitle=None):
    add_textbox(slide, 0.45, 0.22, 12.0, 0.45, title, size=22, bold=True, color=(23, 35, 52))
    if subtitle:
        add_textbox(slide, 0.47, 0.72, 12.0, 0.28, subtitle, size=9.5, color=(92, 101, 114))
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(1.02), Inches(12.4), Inches(0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(58, 111, 174)
    line.line.color.rgb = RGBColor(58, 111, 174)


def bullets(slide, items, x=0.62, y=1.25, w=11.9, h=5.6, size=13):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(size)
        p.font.color.rgb = RGBColor(38, 45, 57)
        p.space_after = Pt(6)
    return box


def table(slide, headers, rows, x, y, w, h, font_size=9):
    shp = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shp.table
    for j, head in enumerate(headers):
        c = tbl.cell(0, j)
        c.text = head
        c.fill.solid()
        c.fill.fore_color.rgb = RGBColor(36, 68, 108)
        for p in c.text_frame.paragraphs:
            p.font.size = Pt(font_size)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            c = tbl.cell(i, j)
            c.text = str(val)
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(font_size)
                p.font.color.rgb = RGBColor(38, 45, 57)
    return shp


def risk_color(sev):
    return {"High": (191, 71, 63), "Medium": (214, 140, 45), "Low": (80, 132, 93)}.get(sev, (90, 90, 90))


def risk_rows():
    return [
        ["High", "FY26 P&L/cash presentation does not reconcile across books and provisional FR", "S2/S4/S6", "Rebuild management accounts from GL + bank + FD schedules before valuation reliance"],
        ["High", "Plaintext tax/GST/TRACES credentials stored in a diligence folder", "S22", "Rotate credentials, remove shared secrets, enforce vault/MFA evidence"],
        ["High", "Revenue evidence is concentrated: unique invoice sample totals INR 9.47m, ~84.7% from Shopsense/Fynd", "S9", "Request complete customer-wise revenue, contracts, collections, and churn bridge"],
        ["Medium", "AR aging shows INR 1.10m due at 28 Feb 2026, including INR 0.59m older than 6 months", "S7/S8", "Confirm post-period collections and provision policy"],
        ["Medium", "Financial workbook contains #REF/formula issues in cash flow sections", "S1/S2", "Obtain locked signed financials and audit trail from accountant"],
        ["Medium", "Go-to-market depends on uncontracted pilots/prospects; pipeline slide lists named prospects but no executed docs for most", "S10/S11", "Confirm stage, owner, next step, commercial terms, and probability for each prospect"],
    ]


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # 1
    s = prs.slides.add_slide(blank)
    add_textbox(s, 0.55, 0.7, 12.2, 0.65, "Vlayx Due Diligence Report", 28, True, (23, 35, 52), PP_ALIGN.CENTER)
    add_textbox(s, 0.55, 1.55, 12.2, 0.32, "Prepared from recursive review of target folder tree and ZIP contents", 13, False, (72, 82, 96), PP_ALIGN.CENTER)
    table(s, ["Scope item", "Result"], [
        ["Target", "/DD/Vlayx inputs - for testing"],
        ["Tree files inventoried", "582 files"],
        ["ZIP-expanded files reviewed", "135 files"],
        ["Extractor errors after remediation", "0"],
        ["Report date", "1 Jun 2026"],
    ], 2.0, 2.35, 9.3, 2.05, 10)
    add_footer(s, ["S0"])

    # 2
    s = prs.slides.add_slide(blank); add_title(s, "Corpus Coverage", "Every file in the tree was inventoried; ZIPs were expanded into the work area for content extraction.")
    table(s, ["File type", "Count"], [["PDF", 496], ["XLSX", 80], ["XLS", 62], ["Tally .1800", 29], ["Tally .TSF", 13], ["Images", 15], ["PPTX", 6], ["TXT/CSV/DOCX/ZIP/metadata", 16]], 0.65, 1.35, 4.0, 3.5, 11)
    bullets(s, [
        "Substantive text extracted from PDFs, Excel workbooks, PowerPoint decks, DOCX, CSV/TXT, Tally text-like files, and ZIP inventories. [S0]",
        "Image files were inventoried and visually reviewed into image_review.csv; ZIP duplicates were tracked in the manifest. [S0/S24]",
        "Full audit trail: manifest.csv, coverage.csv, image_review.csv, extracted_text/*, and zip_expanded/* in DD/Vlayx_DD_work. [S0]",
    ], 5.0, 1.35, 7.4, 3.5, 12.5)
    add_footer(s, ["S0", "S24"])

    # 3
    s = prs.slides.add_slide(blank); add_title(s, "Executive Findings", "Risk discovery view; claims below are document-traced.")
    bullets(s, [
        "Company is incorporated as Valyx Wealthtech Private Limited, CIN U62099KA2023PTC175741, and self-certified as an IT Services/Product Development startup valid to 7 Jul 2033 if eligibility remains met. [S1/S20]",
        "FY25 statutory financials show INR 0.897m revenue from operations, INR 3.155m other income, INR 15.272m expenses, and INR 9.656m loss after deferred-tax credit. [S1]",
        "FY26 YTD accounts are not diligence-ready: books extract shows INR 9.673m operating income while provisional FR shows INR 6.777m total income for the same 28 Feb 2026 cut-off. [S2/S4]",
        "Commercial proof is real but early: current customer ACV list totals INR 8.95m, with pilots/prospects adding INR 11.5m expected first-year ACV, but executed contracts are limited in the corpus. [S10/S14/S16]",
        "Highest immediate control issue: tax/GST/TRACES credentials are stored in plaintext in a document. [S22]",
    ], size=12.3)
    add_footer(s, ["S1", "S2", "S4", "S10", "S14", "S16", "S20", "S22"])

    # 4
    s = prs.slides.add_slide(blank); add_title(s, "Company & Corporate", "Identity, ownership, and governance evidence.")
    bullets(s, [
        "Valyx was incorporated on 8 Jul 2023, with registered office in Bengaluru and business described as information technology software-as-a-service. [S1/S20]",
        "Directors/signatories listed in financials are Avishek Ray (DIN 09146884) and Anirudh Bhargava (DIN 10231484). [S1/S2]",
        "Cap table sheet lists holdings: Avishek 57.56%, Anirudh 19.19%, Waveform 11.65%, Huddle 8.44%, Propel 1.86%, Bharat Founders Fund 1.11%, Sahil Kini 0.18%. [S10]",
        "SSHA dated 28 Aug 2023 states the company business as software platform plus financial services including treasury management and financing discovery. [S19]",
        "Founder employment agreements appoint Avishek as Founder & CEO and Anirudh as Founder & CTO, effective 15 Aug 2023. [S18]",
    ], size=12.3)
    add_footer(s, ["S1", "S2", "S10", "S18", "S19", "S20"])

    # 5
    s = prs.slides.add_slide(blank); add_title(s, "Product & Operations", "Billing/receivables automation proposition.")
    bullets(s, [
        "Mooving order form describes Valyx as a cloud-based billing, revenue management, reconciliation platform automating billing, invoicing, collections, and receivables reconciliation. [S14]",
        "Mooving service term is 1 Apr 2026 to 31 Mar 2027 with capacity for 50,000 invoices and 50,000 payments per month. [S14]",
        "AGI/Hindware scope frames the product as automating payment follow-up, customer on-account suggestions, payment advice reading, invoice knock-off, ledger communication, and TDS follow-up. [S16]",
        "Pricing proposal includes INR 465k one-time setup/configuration fees plus usage fees such as INR 30 per POD, INR 50 per payment advice, and INR 16 per ageing report. [S12]",
        "Operational dependency: org chart places CEO over sales/procurement and CTO/CISO/DevOps over engineering, with design, HR, customer success, and founder's office as functions. [S17]",
    ], size=12.3)
    add_footer(s, ["S12", "S14", "S16", "S17"])

    # 6
    s = prs.slides.add_slide(blank); add_title(s, "Commercial Traction", "Current ACV, pilots, and pipeline.")
    table(s, ["Bucket", "Documented items", "Value"], [
        ["Current customers", "Fynd, LetsTransport, Bhawar, ClickPost, Cygnet, Zippee, Amaze, QED, Vinculum", "INR 8.95m annual revenue list"],
        ["Piloting/strong prospects", "Hindware, AGI, Setu, Synokem, PSB Alliance, Freighttiger, Jeena", "INR 11.5m expected first-year ACV"],
        ["Named pipeline", "HCCB, Movin, Unicommerce, Delhivery, CP Plus, Arvind Fashions, Phicommerce, Grant Thornton", "Stage-level only"],
        ["Outbound engine", "876 enrolled, 90 replies, 40 meetings booked/done in tracker", "No closed-deal count shown"],
    ], 0.55, 1.25, 12.2, 3.0, 9.3)
    bullets(s, [
        "Upsell notes are qualitative for ClickPost and Cygnet; value is not quantified in the customer sheet. [S10]",
        "Pipeline needs conversion proof: the tracker has meetings and replies, but total deals created is blank in the summary area. [S13]",
    ], 0.7, 4.55, 11.7, 1.1, 11.5)
    add_footer(s, ["S10", "S11", "S13"])

    # 7
    s = prs.slides.add_slide(blank); add_title(s, "Financial Performance", "Reported statutory/provisional financials.")
    table(s, ["INR m", "FY25 actuals", "YTD Feb-26 provisional"], [
        ["Revenue from operations", "0.897", "5.663"],
        ["Other income", "3.155", "1.114"],
        ["Total income", "4.052", "6.777"],
        ["Total expenses", "15.272", "18.206"],
        ["Profit before tax", "(11.220)", "(11.429)"],
        ["PAT / current year earnings", "(9.656)", "(11.429)"],
    ], 0.65, 1.25, 6.0, 3.0, 10)
    bullets(s, [
        "Expense base is primarily people: FY26 YTD employee benefits expense is INR 15.788m, 86.7% of total expenses. [S2]",
        "FY25 loss is reduced by INR 1.563m deferred tax credit; no current tax is shown in FY25 or FY26 YTD. [S1/S2]",
        "The audited/provisional workbooks include formulas and #REF references in cash flow areas, so the financial model needs reconstruction before reliance. [S1/S2]",
    ], 7.0, 1.35, 5.7, 3.5, 11.2)
    add_footer(s, ["S1", "S2"])

    # 8
    s = prs.slides.add_slide(blank); add_title(s, "Books Extract Reconciliation", "Material inconsistency at the FY26 YTD cut-off.")
    table(s, ["Metric", "Books extract YTD Feb-26", "Provisional FR YTD Feb-26", "Issue"], [
        ["Sales / revenue from operations", "INR 5.663m", "INR 5.663m", "Agrees"],
        ["Interest/other income", "INR 4.010m interest + INR 0.021m refund", "INR 1.114m other income", "INR ~2.9m unexplained difference"],
        ["Total income", "INR 9.673m", "INR 6.777m", "Does not reconcile"],
        ["Cash/bank/FD presentation", "Bank INR 14.752m plus FD INR 20.000m", "Cash and bank balances INR 42.995m", "Classification/reconciliation gap"],
    ], 0.55, 1.25, 12.2, 3.15, 9.2)
    bullets(s, [
        "This is a diligence blocker for valuation: management accounts, GL, bank statements, FD schedules, and financial statements must be tied out to one cut-off package. [S2/S4/S6]",
    ], 0.75, 4.8, 11.8, 0.8, 12)
    add_footer(s, ["S2", "S4", "S6"])

    # 9
    s = prs.slides.add_slide(blank); add_title(s, "Revenue Quality", "Invoice support and customer concentration.")
    bullets(s, [
        "Unique invoice support reviewed: 48 unique customer invoice PDFs in the FDD invoice folder, totaling INR 9.471m gross invoice value. [S9]",
        "The invoice support is concentrated: Shopsense/Fynd invoices total INR 8.022m, about 84.7% of the unique invoice sample. [S9]",
        "DIPTAB invoices total INR 1.449m in the same unique invoice sample. [S9]",
        "AR aging separately includes SMS Supply Port, Collegedunia, QED, Bhawar, ZFW, Amaze, and DIPTAB, showing the invoice sample is not a complete revenue population. [S8/S9]",
        "Required follow-up: complete customer-wise revenue bridge from GL to invoices to bank receipts and deferred/unbilled revenue schedules. [S4/S8/S9]",
    ], size=12.3)
    add_footer(s, ["S4", "S8", "S9"])

    # 10
    s = prs.slides.add_slide(blank); add_title(s, "Working Capital", "AR, AP, and cash/FD position.")
    table(s, ["Area", "Finding", "Risk"], [
        ["AR", "INR 1.102m total receivables at 28 Feb 2026; INR 0.439m aged 6-12 months and INR 0.151m aged 1-2 years", "Collection/provision risk"],
        ["Specific overdue AR", "Collegedunia and SMS Supply Port include invoices 392-545 days old", "Quality of revenue risk"],
        ["AP", "Trade payable schedule shows INR 22,356 MSME payable at 28 Feb 2026", "Low quantum; verify MSME compliance"],
        ["FDs", "Two INR 10.0m fixed deposits started 28 Nov 2025 at 6.60%, maturity 28 May 2027, no lien marked", "Cash support, but confirm unrestricted use"],
    ], 0.55, 1.25, 12.2, 3.4, 9.3)
    bullets(s, ["Bank confirmation image is dated 21 May 2026 and confirms the FD balances as of 28 Feb 2026. [S24]"], 0.7, 4.9, 11.8, 0.6, 11.5)
    add_footer(s, ["S7", "S8", "S23", "S24"])

    # 11
    s = prs.slides.add_slide(blank); add_title(s, "Tax & Statutory", "Compliance evidence and issues.")
    bullets(s, [
        "GSTIN 29AAJCV5054D1Z6 appears across invoices, GST workbooks, and statutory documents. [S1/S9]",
        "GST/TDS folders include challans, GSTR-2B/GST registers, and TDS payable workbooks through FY26, indicating records exist for statutory verification. [S0]",
        "YTD Feb-26 balance sheet records output IGST INR 10,121, output CGST INR 29,070, output SGST INR 29,070, TDS payable INR 12,302, and TDS on salaries INR 89,627. [S6]",
        "Plaintext credentials are present for Professional Tax, GST, Income Tax, and TRACES; this is a live security/compliance control failure. [S22]",
        "Immediate remediation: rotate all exposed credentials, document MFA/vault controls, and confirm no unauthorized portal activity. [S22]",
    ], size=12.3)
    add_footer(s, ["S0", "S1", "S6", "S9", "S22"])

    # 12
    s = prs.slides.add_slide(blank); add_title(s, "Legal & Contracts", "Executed agreements and open commercial evidence.")
    bullets(s, [
        "Mooving agreement is digitally signed by Avishek Ray and Pooja Agarwal on 20 Feb 2026; service period is 1 Apr 2026 to 31 Mar 2027. [S14]",
        "Awfis agreement provides 8 seats from 18 Nov 2024 to 15 Dec 2025 with 2-month notice period and signed execution metadata. [S15]",
        "SSHA dated 28 Aug 2023 documents pre-seed CCPS investment terms and investor rights. [S19]",
        "Founder employment agreements exist for both founders; each includes full-time duty language and IP/confidentiality provisions. [S18]",
        "Data gap: several current/pipeline customers in KPI materials do not have corresponding executed contracts in the reviewed contract folders. [S10/S14/S16]",
    ], size=12.3)
    add_footer(s, ["S10", "S14", "S15", "S16", "S18", "S19"])

    # 13
    s = prs.slides.add_slide(blank); add_title(s, "People & Organization", "Team structure and hiring needs.")
    bullets(s, [
        "Org chart shows two-founder leadership: Anirudh over CTO/CISO/DevOps and engineering; Avishek over CEO, sales, and procurement. [S17]",
        "The same org chart lists engineering, design, HR, customer success, and founder's office as functions, but does not show headcount by person or reporting line depth. [S17]",
        "Leadership open roles slide identifies six critical hires: backend billing lead engineer, backend receivable lead engineer, UX design lead, sales lead, marketing lead, customer support lead. [S17]",
        "Payroll books show employee benefits as the largest expense line; FY26 YTD employee benefits were INR 15.788m. [S2]",
        "Request full employee roster, ESOP/equity grants, offer letters, payroll statutory filings, attrition, and founder vesting status. [S2/S17/S18/S19]",
    ], size=12.3)
    add_footer(s, ["S2", "S17", "S18", "S19"])

    # 14
    s = prs.slides.add_slide(blank); add_title(s, "Technology & Security", "Product controls and diligence concerns.")
    bullets(s, [
        "Mobile device policy is based on ISO/IEC 27001:2022, document no. Valyx/II/ISM/POL-12, version 1.0, effective 30 Jun 2025. [S21]",
        "The same policy lists CISO as approver and classifies the document as internal. [S21]",
        "Security posture is inconsistent with policy maturity because tax/GST/TRACES credentials are exposed in plaintext in the diligence corpus. [S22]",
        "Mooving SaaS terms hold customer responsible for account/password security and equipment; Valyx should show equivalent internal access controls for its own systems. [S14/S22]",
        "Data gap: no SOC2/ISO certificate, pen test, cloud architecture, access logs, SDLC evidence, incident register, or DPA/security addendum was found in the reviewed corpus. [S0/S21/S22]",
    ], size=12.3)
    add_footer(s, ["S0", "S14", "S21", "S22"])

    # 15
    s = prs.slides.add_slide(blank); add_title(s, "Market, Valuation & Plan", "Projection assumptions need validation.")
    bullets(s, [
        "Projection workbook assumes FY26-FY31 annual revenue grows from USD 0.4m to USD 37.864m, translating to INR 3.36cr to INR 318.06cr. [S10]",
        "Projection model assumes FY26 10 users growing to 400 by FY31 and software ACV rising from USD 40k to USD 80.454k. [S10]",
        "Model lists TAM assumption of 45,000 companies in INR 30-500cr turnover range and notes external TAM counts, but no independently sourced market study is tied to the model. [S10]",
        "Comparable deals tab cites 20x-50x revenue-to-valuation multiples for billing/AR/procurement automation companies. [S10]",
        "Risk: plan depends on conversion of current pipeline and high ACVs while FY26 YTD revenue from operations is INR 5.663m. [S2/S10]",
    ], size=12.3)
    add_footer(s, ["S2", "S10"])

    # 16
    s = prs.slides.add_slide(blank); add_title(s, "Inconsistencies", "Items requiring reconciliation before deal reliance.")
    bullets(s, [
        "FY26 income mismatch: books extract reports INR 5.663m sales plus INR 4.010m interest income, while provisional FR reports INR 5.663m revenue and INR 1.114m other income. [S2/S4]",
        "FY26 cash/FD mismatch: books balance sheet presents bank balances plus two INR 10m FDs separately, while provisional FR presents INR 42.995m cash and bank balances. [S2/S6]",
        "Financial workbook integrity issue: cash flow worksheets include #REF references, including operating cash flow lines. [S1/S2]",
        "Invoice support completeness issue: invoice folder sample has two main customers, while AR aging includes additional overdue customers not represented as a complete invoice pack. [S8/S9]",
        "Policy-control mismatch: an ISO-based mobile device policy exists, but plaintext statutory credentials are included in the data room. [S21/S22]",
    ], size=12.2)
    add_footer(s, ["S1", "S2", "S4", "S6", "S8", "S9", "S21", "S22"])

    # 17
    s = prs.slides.add_slide(blank); add_title(s, "Risk Register", "Prioritized diligence risks.")
    table(s, ["Severity", "Risk", "Src", "Recommended action"], risk_rows(), 0.35, 1.15, 12.65, 4.9, 7.8)
    add_footer(s, ["S1", "S2", "S4", "S6", "S7", "S8", "S9", "S10", "S13", "S22"])

    # 18
    s = prs.slides.add_slide(blank); add_title(s, "Data Gaps & Confirmatory Requests", "Open items before investment/closing.")
    bullets(s, [
        "Financial: locked FY26 management accounts, GL-to-FS mapping, bank reconciliation, FD confirmations, deferred tax support, revenue recognition memo. [S1/S2/S4/S6/S24]",
        "Revenue: complete contract folder for every current customer; invoice-to-bank collections bridge; ARR/MRR/churn cohort; unbilled/deferred revenue schedule. [S8/S9/S10/S14]",
        "Legal: cap table from statutory registers, latest AoA/MoA, board minutes after pre-seed, conditions subsequent tracker, IP assignment for employees/contractors. [S10/S19]",
        "Tax: GST/TDS/PT returns with challan reconciliation and portal access logs after credential rotation. [S0/S22]",
        "Security/product: architecture diagram, cloud access list, code/IP ownership, data processing agreements, pen-test/SOC2/ISO evidence, backup/DR proof. [S0/S21/S22]",
        "Operations/people: current org roster, payroll compliance, offer letters, contractor agreements, hiring plan tied to burn forecast. [S2/S17/S18]",
    ], size=11.5)
    add_footer(s, ["S0", "S1", "S2", "S4", "S6", "S8", "S9", "S10", "S14", "S17", "S18", "S19", "S21", "S22", "S24"])

    # 19
    s = prs.slides.add_slide(blank); add_title(s, "Source Register I", "Source IDs used in this deck.")
    rows = [[sid, sources[sid]] for sid in list(sources.keys())[:13]]
    table(s, ["ID", "Source file / corpus artifact"], rows, 0.35, 1.1, 12.65, 5.5, 7.8)
    add_footer(s, ["S0"])

    # 20
    s = prs.slides.add_slide(blank); add_title(s, "Source Register II", "Source IDs used in this deck.")
    rows = [[sid, sources[sid]] for sid in list(sources.keys())[13:]]
    table(s, ["ID", "Source file / corpus artifact"], rows, 0.35, 1.1, 12.65, 5.2, 7.8)
    add_footer(s, ["S0"])

    # 21
    s = prs.slides.add_slide(blank); add_title(s, "Coverage Appendix", "Inventory evidence generated from recursive extraction.")
    bullets(s, [
        "Full tree inventory: DD/Vlayx_DD_work/output/manifest.csv. [S0]",
        "Extraction status and file-type counts: DD/Vlayx_DD_work/output/coverage.csv. [S0]",
        "Per-file extracted content: DD/Vlayx_DD_work/extracted_text/*.txt; image visual review notes: DD/Vlayx_DD_work/output/image_review.csv. [S0]",
        "Expanded archive contents: DD/Vlayx_DD_work/zip_expanded/*. [S0]",
        "All 582 files in the target folder tree and 135 ZIP-contained files were represented in the manifest with SHA-256, size, extractor, status, and extracted text path. [S0]",
    ], size=12.3)
    add_footer(s, ["S0"])

    prs.save(PPTX)

    with (OUT / "source_register.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "source"])
        w.writerows(sources.items())

    print(PPTX)


if __name__ == "__main__":
    main()
