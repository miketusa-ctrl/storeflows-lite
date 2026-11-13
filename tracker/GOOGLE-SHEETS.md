# Using the tracker in Google Sheets

The tracker is built in Excel format (`harlo-storeflows-tracker.xlsx`) with live formulas. You have two ways to use it in Google Sheets.

## Option A (recommended): upload the XLSX

1. Open Google Drive → **New → File upload** → choose `harlo-storeflows-tracker.xlsx`.
2. Right-click the file → **Open with → Google Sheets**.
3. **File → Save as Google Sheets** so you have an editable copy. All tabs, formats and formulas come across.
4. Edit only the shaded input cells. The Settings tab controls the test window, holdout share and minimum sample sizes.

## Option B: import the CSVs

Use this if you only want the Flow log or Daily tab, or your Drive blocks Office uploads.

1. Create a new blank Google Sheet.
2. **File → Import → Upload** → choose `tracker-flow-log.csv`.
3. Import location: **Replace current sheet** (or **Insert new sheet(s)**). Separator: **Comma**. Leave **Convert text to numbers, dates, and formulas** ticked so the formulas calculate.
4. Repeat for `tracker-daily.csv` into a new sheet if you want the day-by-day log.

CSV notes:
- CSV files cannot reference other tabs, so the CSV formulas have the Settings values written in (21-day window, minimum 100 holdout recipients, minimum 20 combined orders). To change them, edit the numbers inside the formulas in columns D and W, or use Option A.
- Keep the first three rows in place. The formulas expect the header on row 4 and data from row 5 (Daily tab: start date in cell B2).
- If a date shows as text, select column C → **Format → Number → Date**.

## Checking the math

`scripts/verify_formulas.py` recalculates every workbook and formula CSV in LibreOffice and fails on any `#DIV/0!`, `#REF!`, `#VALUE!`, `#NAME?` or `#N/A`. It also runs a blank-input stress test. Divisions are guarded with `IF(denominator>0, …, 0)` and RPR lift shows `n/a` when holdout revenue is zero.

## What the numbers mean

| Column | Formula idea |
|---|---|
| Conv rate | orders ÷ recipients (treatment and holdout separately) |
| RPR | revenue ÷ recipients |
| RPR lift % | (RPR treatment − RPR holdout) ÷ RPR holdout |
| Incremental revenue | (RPR treatment − RPR holdout) × treatment recipients |
| Net of discount | incremental revenue − discount cost |
| z score | two-proportion z-test on conversion rate |
| Confidence note | holdout and order minimums first, then z ≥ 2.576 / 1.96 / 1.645 |

This is a practical estimate, not a formal experiment readout. Small holdouts and seasonal swings can mislead, so results vary and should be re-checked over more than one window.
