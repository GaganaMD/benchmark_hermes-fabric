# Tally vs Blinkit Reconciliation Report

Used Fabric (`fabric -p create_summary`) after the reconciliation pass to sanity-check and sharpen the executive summary. Matching logic: Tally `Vch No.` = Blinkit `Inv No`; amount difference = Blinkit Amount - Tally Debit; absolute difference <= INR 1.00 treated as rounding OK. Blinkit TDS reversal rows are classified separately, not as invoices.

## Executive Summary
- Tally invoice rows: 58 totaling INR 3449187.48.
- Blinkit bill rows excluding TDS reversals: 30 totaling INR 2324215.04.
- Blinkit TDS reversal rows: 15 totaling INR 157.32.
- Matched within rounding tolerance: 26 invoices.
- Amount mismatches above INR 1.00: 3 invoices; total absolute variance INR 38.57.
- Probable invoice-number mismatch: 1 pair.
- Unresolved Tally-only after adjusting invoice mismatch: 28 invoices totaling INR 1125014.00.
- Unresolved Blinkit-only after adjusting invoice mismatch: 0 invoices.

## Amount Mismatches
| Invoice | Tally date | Blinkit date | Tally INR | Blinkit INR | Diff |
| --- | --- | --- | --- | --- | --- |
| NY/23-24/091 | 27-May-23 | 17/08/2023 | 65050.00 | 65085.58 | 35.58 |
| NY/23-24/308 | 6-Oct-23 | 15/12/2023 | 265155.00 | 265156.29 | 1.29 |
| NY/23-24/444 | 29-Feb-24 | 22/03/2024 | 231804.00 | 231805.70 | 1.70 |

## Probable Invoice Number Mismatch
| Tally invoice | Blinkit invoice | Tally INR | Blinkit INR | Diff | Evidence |
| --- | --- | --- | --- | --- | --- |
| NY/23-24/023 | NY/23-24/028 | 240981.00 | 240981.55 | 0.55 | same/near-same amount but invoice no differs |

## Unresolved Tally-only Invoices
| Invoice | Date | INR |
| --- | --- | --- |
| NY/23-24/097 | 31-May-23 | 43239.00 |
| NY/23-24/098 | 31-May-23 | 59098.00 |
| NY/23-24/161 | 29-Jun-23 | 55347.00 |
| NY/23-24/208 | 17-Jul-23 | 32910.00 |
| NY/23-24/214 | 21-Jul-23 | 17277.00 |
| NY/23-24/239 | 27-Jul-23 | 9757.00 |
| NY/23-24/240 | 31-Jul-23 | 34321.00 |
| NY/23-24/250 | 11-Aug-23 | 19570.00 |
| NY/23-24/251 | 11-Aug-23 | 14960.00 |
| NY/23-24/264 | 25-Aug-23 | 22475.00 |
| NY/23-24/270 | 30-Aug-23 | 44897.00 |
| NY/23-24/271 | 30-Aug-23 | 57618.00 |
| NY/23-24/272 | 30-Aug-23 | 36141.00 |
| NY/23-24/274 | 31-Aug-23 | 38462.00 |
| NY/23-24/275 | 31-Aug-23 | 26869.00 |
| NY/23-24/276 | 31-Aug-23 | 25802.00 |
| NY/23-24/293 | 21-Sep-23 | 55400.00 |
| NY/23-24/298 | 28-Sep-23 | 26827.00 |
| NY/23-24/299 | 28-Sep-23 | 71408.00 |
| NY/23-24/319 | 24-Oct-23 | 110709.00 |
| NY/23-24/353 | 2-Nov-23 | 30474.00 |
| NY/23-24/366 | 24-Nov-23 | 74498.00 |
| NY/23-24/369 | 24-Nov-23 | 31071.00 |
| NY/23-24/411 | 19-Jan-24 | 58210.00 |
| NY/23-24/422 | 31-Jan-24 | 30910.00 |
| NY/23-24/440 | 26-Feb-24 | 56092.00 |
| NY/23-24/446 | 28-Feb-24 | 22628.00 |
| NY/23-24/465 | 15-Mar-24 | 18044.00 |

## Matched Invoices - Rounding OK
| Invoice | Tally INR | Blinkit INR | Diff |
| --- | --- | --- | --- |
| NY/23-24/092 | 43758.00 | 43758.04 | 0.04 |
| NY/23-24/122 | 31469.00 | 31468.78 | -0.22 |
| NY/23-24/123 | 26066.00 | 26066.35 | 0.35 |
| NY/23-24/149 | 114456.00 | 114456.37 | 0.37 |
| NY/23-24/202 | 30726.00 | 30725.86 | -0.14 |
| NY/23-24/215 | 18985.00 | 18984.63 | -0.37 |
| NY/23-24/237 | 62565.00 | 62564.70 | -0.30 |
| NY/23-24/238 | 32837.00 | 32837.58 | 0.58 |
| NY/23-24/257 | 45314.00 | 45313.71 | -0.29 |
| NY/23-24/262 | 113985.00 | 113985.29 | 0.29 |
| NY/23-24/282 | 57674.00 | 57674.01 | 0.01 |
| NY/23-24/287 | 19907.84 | 19908.07 | 0.23 |
| NY/23-24/288 | 17232.64 | 17232.55 | -0.09 |
| NY/23-24/374 | 118111.00 | 118111.78 | 0.78 |
| NY/23-24/378 | 64772.00 | 64771.68 | -0.32 |
| NY/23-24/387 | 28195.00 | 28195.31 | 0.31 |
| NY/23-24/398 | 65322.00 | 65321.98 | -0.02 |
| NY/23-24/402 | 49899.00 | 49898.72 | -0.28 |
| NY/23-24/409 | 60923.00 | 60923.45 | 0.45 |
| NY/23-24/416 | 32121.00 | 32120.68 | -0.32 |
| NY/23-24/433 | 118988.00 | 118988.14 | 0.14 |
| NY/23-24/438 | 44448.00 | 44448.62 | 0.62 |
| NY/23-24/491 | 83343.00 | 83343.63 | 0.63 |
| NY/24-25/17 | 47426.00 | 47425.88 | -0.12 |
| NY/24-25/23 | 92331.00 | 92330.70 | -0.30 |
| NY/24-25/25 | 100329.00 | 100329.41 | 0.41 |

## Blinkit TDS Reversals
| Date | Amount INR | Description |
| --- | --- | --- |
| 30/06/2023 | 1.64 | TDS-REV-JUNE-60 - due on 30/06/2023 |
| 31/07/2023 | 0.57 | TDS-REV-JUL-125 - due on 31/07/2023 |
| 31/08/2023 | 5.76 | TDS-REV-AUG-20 - due on 31/08/2023 |
| 31/08/2023 | 5.01 | TDS-REV-AUG-390 - due on 31/08/2023 |
| 31/08/2023 | 23.04 | TDS-REV-AUG-414 - due on 31/08/2023 |
| 31/08/2023 | 35.46 | TDS-REV-AUG-516 - due on 31/08/2023 |
| 31/08/2023 | 8.82 | TDS-REV-AUG-559 - due on 31/08/2023 |
| 31/08/2023 | 4.73 | TDS-REV-AUG-599 - due on 31/08/2023 |
| 30/09/2023 | 3.01 | TDS-REV-SEP-57 - due on 30/09/2023 |
| 30/09/2023 | 11.62 | TDS-REV-SEP-153 - due on 30/09/2023 |
| 31/10/2023 | 9.40 | TDS-REV-OCT-67 - due on 31/10/2023 |
| 31/12/2023 | 38.92 | TDS-REV-DEC-80 - due on 31/12/2023 |
| 31/01/2024 | 3.16 | TDS-REV-JAN-78 - due on 31/01/2024 |
| 29/02/2024 | 4.99 | TDS-REV-FEB-76 - due on 29/02/2024 |
| 31/03/2024 | 1.19 | TDS-REV-MAR-78 - due on 31/03/2024 |
