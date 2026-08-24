# Sample Client Reports — Analysis

Source folder: `docs/reference docs/reports/` (10 files: 4 PDFs + 6 JPEGs)

Per `docs/reference docs/project docs/project planning and execution.txt`, these are the
**"3–4 representative IVF reports"** the POC should be validated against — one digital PDF,
one complex/multi-page, and printed-report-photographed-by-phone variants. This file maps
each raw file to what it actually is, so extraction/summarization logic can be designed
around real report shapes rather than assumptions.

## Headline finding

**Update:** the Domain Knowledge doc has since been extended with a "Pregnancy/Antenatal
Monitoring" section (see [[ivf-domain-knowledge]]) specifically to cover this gap — as of
that update, coverage is now:

| Report (patient) | Covered by domain doc? |
|---|---|
| InsighT NIPS (Mital) | ✅ matches "NIPT / Cell-Free DNA Screening" row |
| First-Trimester Combined Screening (Tinkal) | ✅ matches "Nuchal Translucency (NT) / Combined Screening" row |
| CBC + Random Blood Glucose (Priyal) | ✅ matches "CBC / Hemoglobin" + "Blood Glucose / Diabetes Screening" rows |
| TSH + Prolactin (Priyal) | ✅ already covered by the original pre-IVF panel table |
| Hemoglobin Electrophoresis / thalassemia screen (Nisha Nath Yogi) | ✅ now has its own named row — "Hemoglobin Electrophoresis (HbA/HbA2/HbF by HPLC)" added to the Indicated-only tests table in [[ivf-domain-knowledge]] |

Originally (before that update), 3 of 4 distinct patients in this sample had
**prenatal/pregnancy-monitoring reports** (post-conception testing) rather than the classic
pre-IVF workup panel — which is what prompted the doc update. All reports share the same
referring doctor (**Dr. Jaydev Dhameliya**) and lab group (**Zenex Path Lab, a unit of
Candor IVF Center**, Surat), routed to specialist partner labs (Sorus Diagnostics for
immunology/hematology, Revvity/SN Genelabs and Lilac Insights for prenatal genetic
screening).

All 5 report types in this sample set are now explicitly named somewhere in the domain
reference — no remaining open items from this comparison.

## File → report mapping

| # | File | Format | Patient | Sex | Report Type | Stage | Pages |
|---|---|---|---|---|---|---|---|
| 1 | `Mrs Mital Janak Ghevariya_WITHOUT_LETTERHEAD_REPORT.pdf` | Digital PDF (native, letterhead stripped) | Mital Janak Ghevariya | F | InsighT NIPS (Non-Invasive Prenatal Screening) | During pregnancy (13w+3d GA), post-conception | 5 |
| 2 | `TestReport_TINKAL DIVYANG SANGANI_...pdf` | Digital PDF (native, Revvity/GeneLab template) | Tinkal Divyang Sangani | F | Prenatal First Trimester (Combined) Screening | During pregnancy (13w GA), post-conception | 5 |
| 3 | `WLh_PRIYAL_KALTHIYA_DR_JAYDEV_...PDF` | Digital PDF (native, Zenex Path Lab template) | Priyal Kalthiya | F | Haematology + Biochemistry (CBC + RBS) | Pre-IVF general health screening | 1 |
| 4 | `PRIYAL KALTHIYA (1).pdf` | Digital PDF (native, Sorus Diagnostics template) | Priyal Kalthiya | F | Immunology — TSH (Ultra Sensitive) + Serum Prolactin | Pre-IVF hormonal evaluation | 3 |
| 5 | `WhatsApp Image ...31.jpeg` | Phone photo of printout | Tinkal Divyang Sangani | F | Prenatal First Trimester Screening — page 2 (probability table, hand-highlighted) | Same as #2 | 1 of 5 |
| 6 | `WhatsApp Image ...31 (1).jpeg` | Phone photo of printout | Tinkal Divyang Sangani | F | Prenatal First Trimester Screening — page 1 (patient/pregnancy/USG details, hand-highlighted) | Same as #2 | 1 of 5 |
| 7 | `WhatsApp Image ...32.jpeg` | Phone photo of printout | Mital Janak Ghevariya | F | InsighT NIPS — page 1 (test results, hand-highlighted) | Same as #1 | 1 of 5 |
| 8 | `WhatsApp Image ...32 (1).jpeg` | Phone photo of printout | Priyal Kalthiya | F | Immunology — TSH page 1 (hand-highlighted) | Same as #4 | 1 of 3 |
| 9 | `WhatsApp Image ...33.jpeg` | Phone photo of printout | Priyal Kalthiya | F | Immunology — Prolactin page 2 (hand-highlighted) | Same as #4 | 2 of 3 |
| 10 | `WhatsApp Image ...33 (1).jpeg` | Phone photo of printout | **Nisha Nath Yogi** (new patient, no digital counterpart in this set) | F | Hematology — Hemoglobin Electrophoresis by HPLC (HbA/HbA2/HbF — thalassemia screening) | Pre-IVF genetic/carrier-type screening | 1 of 3 |

All patients in this sample set are female — no male-partner reports (semen analysis, male
hormonal profile) were provided. Worth flagging to the client as a gap in the sample set,
since the POC should eventually handle male-partner reports too.

The JPEGs are exactly the "printed report → phone photo" test case called for in the
execution plan: mobile-camera lighting/glare, visible paper fold/curl, and hand-written
highlighter marks and margin annotations (doctor/staff circling key values, blank
`Name/Age/Date` counselling-note lines at the bottom) that a real OCR pipeline will have to
tolerate or ignore.

## Per-report detail

### 1 & 5/6 — InsighT NIPS Report (Mital Janak Ghevariya)
- **Lab:** Lilac Insights Pvt. Ltd. (via Zenex Path Lab / Candor IVF Center), Navi Mumbai.
- **What it is:** Non-Invasive Prenatal Screening (cfDNA from maternal blood, NGS-based) for
  common aneuploidies and sex-chromosome aneuploidies.
- **Why ordered:** Referral reason stated on report — "USG at 13 weeks 2 days shows increased
  NT 3mm at CRL of 68mm" (an abnormal ultrasound nuchal translucency finding prompted this
  confirmatory screen).
- **Key result fields:** Trisomy 21/18/13 risk (Low/Increased), sex-chromosome aneuploidy
  risk (XO/XXY/XYY/XXX), Fetal cf-DNA % (7.47%, flagged sufficient for analysis).
- **Result in this case:** All conditions **Low Risk**; recommendation is routine genetic
  counselling to explain the result (not because of an abnormal finding).
- **Structure:** cover/results page → recommendations & performance/validation stats →
  marketing/methodology page → interpretation flowchart → references & disclaimers/sign-off.
  Only page 1 (and its highlighted photo counterpart) carries patient-specific data useful
  for a summary — pages 2–5 are boilerplate methodology/marketing/legal that a summarizer
  should down-weight or drop entirely.
- **Extraction risk:** the report explicitly states sex of fetus cannot be disclosed
  (PC-PNDT Act 2003) — a summarizer must never infer/state fetal sex even if derivable from
  X/Y-linked risk categories.

### 2 & 5/6 — Prenatal First Trimester Screening Report (Tinkal Divyang Sangani)
- **Lab:** Revvity / SN Genelabs Pvt Ltd (Surat), via Candor IVF referral.
- **What it is:** Combined first-trimester biochemical + ultrasound screening (hCGb, PAPP-A,
  NT, nasal bone) computing Down/Edward/Patau syndrome probability — distinct methodology
  from NIPS (older serum-marker + NT combined test vs. cfDNA sequencing).
- **Key fields:** LMP date, calculated EDD, gestational age, CRL/NT/nasal-bone ultrasound
  values, hCGb & PAPP-A levels with corrected MoM, per-condition probability (By Age / Final
  / Cut-off / Interpretation).
- **Result in this case:** All three conditions **Low** probability (e.g. T21 final risk
  1:34170 vs cutoff 1:250).
- **Structure:** patient/pregnancy/ultrasound details → test values & probability table with
  charts → condition-by-condition interpretation + general interpretation guide → sign-off →
  a generic "how to read your result" patient-education sheet (page 5, non-patient-specific,
  should be excluded from a per-patient summary).
- **Note:** this is a *different, complementary* screening pathway to NIPS — a summarizer
  should recognize both as "aneuploidy screening" but not conflate their methodologies or
  probability scales (this one reports odds like 1:34170; NIPS reports Low/Increased Risk
  categorically).

### 3 — Haematology + Biochemistry Report (Priyal Kalthiya)
- **Lab:** Zenex Path Lab (Candor IVF Center), Surat. Referred by Dr. Jaydev Dhameliya.
- **What it is:** Routine CBC (haemoglobin, RBC/PCV/indices, WBC differential, platelets) +
  Random Blood Glucose + attempted Urine Glucose (sample not received) — general health
  screening, part of the core pre-IVF panel.
- **Notable abnormal values (flagged with arrows on the original):** low Haemoglobin
  (10.10 vs 12–16 gm%), low PCV/MCV/MCH/MCHC (microcytic hypochromic picture consistent with
  possible iron-deficiency anemia), high RDW, high Neutrophils/low Lymphocytes, low Monocytes.
  This is a good exemplar for testing the summarizer's "abnormal/critical findings" section —
  the source report itself uses up/down arrows and bold to flag out-of-range values, which
  extraction logic should key off of.
- **Structure:** single dense page, no boilerplate — the simplest/cleanest report in the set.

### 4 & 5/6 — Immunology Report: TSH + Prolactin (Priyal Kalthiya)
- **Lab:** Sorus Diagnostics, Surat, via Zenex Path Lab.
- **What it is:** Two separate hormone assays bundled in one 3-page report — TSH (Ultra
  Sensitive) and Serum Prolactin — both explicitly named in the core pre-IVF panel (thyroid
  function + prolactin, [[ivf-domain-knowledge]]).
- **Key fields:** result, unit, biological reference interval (which differs for
  pregnant vs non-pregnant for Prolactin — extraction must capture that the range is
  conditional).
- **Result in this case:** TSH 0.75 mIU/L (within 0.270–4.20) and Prolactin 11.0 ng/mL
  (within nonpregnant range 6.0–29.9) — both normal.
- **Structure:** each parameter gets its own page with a long clinical-reference essay
  (mechanism, clinical use, causes of increased/decreased levels) — almost entirely
  boilerplate. The actual patient result is a single row per page; the surrounding
  paragraphs should be excluded from the summary, similar to the NIPS/screening
  boilerplate pages.

### 10 — Hemoglobin Electrophoresis by HPLC (Nisha Nath Yogi) — image only
- **Lab:** Sorus Diagnostics (same group), Surat.
- **What it is:** Thalassemia/hemoglobinopathy carrier screen — HbA, HbA2, HbF fractions by
  HPLC. Relevant to the "genetic carrier screening" line item in the core/indicated pre-IVF
  panel.
- **Result in this case:** Hb A 96.8% (95–98, normal), Hb A2 2.0% (1.5–3.5, normal), **Hb F
  1.2%** (flagged **H** for high, ref. 0.0–1.0) — interpretation printed on the report:
  "Findings are suggestive of normal hemoglobin chromatograph," i.e. the single high HbF
  flag is not read by the lab as clinically significant on its own.
  This is a good adversarial test case: an individual value is out-of-range but the report's
  own narrative interpretation calls the overall picture normal — a good summarizer must
  surface the lab's interpretation, not just re-flag every out-of-range number as if it were
  a finding of concern.
- Only available as a phone-photographed page in this set (no clean digital PDF for this
  patient) — useful as the "scanned/photographed, no digital source" test case.

## Cross-cutting observations for extraction/summarization design

1. **Boilerplate is the majority of page count.** Across the 5-page NIPS and 5-page
   first-trimester reports, only 1 page (sometimes split across 2 in the photographed
   version) carries patient-specific data; the rest is methodology, marketing, generic
   interpretation guides, and legal disclaimers. The extraction step should identify and
   drop/deprioritize this before summarization, both to save tokens and to avoid the LLM
   summarizing boilerplate as if it were a finding.
2. **Reference ranges are sometimes conditional** (e.g. Prolactin differs for pregnant vs.
   non-pregnant women) — the summarizer needs the patient's pregnancy status to correctly
   judge normal/abnormal, not just compare the number to a single static range.
3. **Reports already self-flag abnormal values** (arrows, bold, "H"/"L" markers, or an
   explicit narrative "Interpretation" line) — extraction should capture these lab-provided
   flags directly rather than re-deriving normal/abnormal purely from the numeric range,
   since (as in the HbF case) the lab's own clinical interpretation can override a
   raw out-of-range flag.
4. **Legally sensitive content exists** (PC-PNDT Act 2003 fetal-sex non-disclosure on the
   NIPS report) — the system must never fill in or infer information the source report
   explicitly withholds.
5. **Real-world OCR conditions confirmed:** the 6 JPEGs show glare, slight skew, visible
   paper curl/fold, and highlighter/pen annotations over printed text — exactly the
   "poorly formatted/scanned" and "printed report photographed by phone" cases the
   execution plan calls for testing against.
6. **All 4 distinct patients here are female / pregnancy-related.** No male-partner
   (semen analysis) or ovarian-reserve (AMH/FSH/LH) report is present in the sample set —
   flag this to the client as a gap before treating this sample set as fully representative.

## Suggested summary-schema fields (draft, based on what's actually present)

Given the report types actually seen, a practitioner-facing summary schema should probably
capture, per report:
- Patient name, age/DOB, sex
- Report type / test name(s) performed
- Referring doctor, lab, collection & report dates
- Pregnancy context if applicable (GA, LMP, EDD, gravida detail) — since reference ranges
  and clinical meaning depend on it
- Each parameter: value, unit, reference range, in/out-of-range flag as printed by the lab
- The lab's own narrative interpretation/conclusion line, verbatim where present (don't let
  the LLM override it)
- Recommendations / next steps stated on the report
- Explicit "not stated" for anything legally withheld (e.g. fetal sex) rather than omitting
  the field silently
