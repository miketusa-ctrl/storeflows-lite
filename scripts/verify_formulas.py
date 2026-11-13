#!/usr/bin/env python3
"""Recalculate every kit workbook (and formula CSV) with LibreOffice headless and
fail on any spreadsheet error value (#DIV/0!, #REF!, #VALUE!, #NAME?, #N/A, #NUM!)
or any formula cell left without a computed value.

Usage: python3 scripts/verify_formulas.py [--root PATH] [--dump]   (needs openpyxl + soffice on PATH)
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
ERRORS = ("#DIV/0!", "#REF!", "#VALUE!", "#NAME?", "#N/A", "#NUM!", "#NULL!", "Err:")
SKIP = {".git", "dist", "__pycache__", ".scratch"}


def _discover(root: Path, pattern: str) -> list[Path]:
    return sorted(p for p in root.rglob(pattern) if not any(s in SKIP for s in p.relative_to(root).parts))


def targets(root: Path) -> tuple[list[Path], list[Path], Path | None]:
    """Every workbook and CSV under the kit root (works in the repo and in an unzipped tier)."""
    xlsx = [p for p in _discover(root, "*.xlsx") if not p.name.startswith("~$")]
    csvs = _discover(root, "*.csv")
    trackers = [p for p in xlsx if p.name.endswith("-tracker.xlsx") and "example" not in p.relative_to(root).parts]
    return xlsx, csvs, (trackers[0] if trackers else None)


def recalc(src: Path, tmp: Path, csv_in: bool = False) -> Path:
    work = tmp / src.name
    shutil.copy(src, work)
    args = ["soffice", "--headless", "--norestore", "--convert-to", "xlsx", "--outdir", str(tmp / "out")]
    if csv_in:
        # 44=comma, 34=quote, 76=UTF-8; 9th token true = evaluate formulas
        args[3:3] = ["--infilter=CSV:44,34,76,1,,0,false,true,false,false,false,-1"]
    subprocess.run(args + [str(work)], check=True, capture_output=True, timeout=180)
    return tmp / "out" / (src.stem + ".xlsx")


def scan(original: Path, recalced: Path, csv_mode: bool = False) -> tuple[int, int, list[str]]:
    problems, formulas, checked = [], 0, 0
    if csv_mode:
        import csv as _csv
        f_rows = list(_csv.reader(original.open(encoding="utf-8")))
        fwb = None
    else:
        fwb = load_workbook(original)  # formulas
    vwb = load_workbook(recalced, data_only=True)  # values after LibreOffice recalculation
    sheets = vwb.sheetnames
    for name in sheets:
        vws = vwb[name]
        for row in vws.iter_rows():
            for c in row:
                v = c.value
                checked += 1
                if fwb is not None:
                    fv = fwb[name][c.coordinate].value
                else:
                    try:
                        fv = f_rows[c.row - 1][c.column - 1]
                    except IndexError:
                        fv = None
                is_formula = isinstance(fv, str) and fv.startswith("=")
                if is_formula:
                    formulas += 1
                    if v is None or (isinstance(v, str) and v.startswith("=")):
                        problems.append(f"{original.name}!{name}!{c.coordinate}: formula not evaluated ({fv})")
                if isinstance(v, str) and any(v.startswith(e) for e in ERRORS):
                    problems.append(f"{original.name}!{name}!{c.coordinate}: {v} ({fv})")
    return formulas, checked, problems


def dump(recalced: Path, sheet: str, first: int, last: int, cols: str) -> None:
    ws = load_workbook(recalced, data_only=True)[sheet]
    for r in range(first, last + 1):
        vals = []
        for col in cols:
            v = ws[f"{col}{r}"].value
            vals.append(f"{v:.3f}" if isinstance(v, float) else str(v))
        print("   ", " | ".join(vals))


def main() -> int:
    if not shutil.which("soffice"):
        print("soffice (LibreOffice) not found; cannot recalculate.")
        return 2
    global ROOT
    if "--root" in sys.argv:
        ROOT = Path(sys.argv[sys.argv.index("--root") + 1]).resolve()
    xlsx_targets, csv_targets, tracker = targets(ROOT)
    if not xlsx_targets and not csv_targets:
        print("no workbooks or CSVs found")
        return 2
    total_f, all_problems = 0, []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for x in xlsx_targets:
            rc = recalc(x, tmp)
            f, n, p = scan(x, rc)
            if "tracker" in x.name and "--dump" in sys.argv:
                print("   Flow log A,L,M,N,O,P,R,S,U,W (rows 5-11):")
                dump(rc, "Flow log", 5, 11, "ALMNOPRSUW")
            print(f"[xlsx] {x.relative_to(ROOT)}: {f} formulas recalculated, {len(p)} problems")
            total_f += f
            all_problems += p
        # Stress test: blank every shaded input cell in the tracker and recalc (empty-sheet case).
        src = tracker
        wb = load_workbook(src) if src else None
        if wb is None:
            print("[xlsx] no template tracker found; stress test skipped")
        if wb is not None:
            cleared = 0
            for ws in wb.worksheets:
                if ws.title in ("Settings", "How to use"):
                    continue
                for row in ws.iter_rows():
                    for c in row:
                        if c.fill is not None and c.fill.fgColor is not None and str(c.fill.fgColor.rgb).endswith("FFF6E5") and not str(c.value or "").startswith("="):
                            if c.column_letter not in ("A", "B") or ws.title == "Weekly RPR":
                                c.value = None
                                cleared += 1
            (tmp / "stress").mkdir(exist_ok=True)
            blank = tmp / "stress" / "blank-inputs-tracker.xlsx"
            wb.save(blank)
            f, n, p = scan(blank, recalc(blank, tmp))
            print(f"[xlsx] blank-input stress test ({cleared} inputs cleared): {f} formulas recalculated, {len(p)} problems")
            total_f += f
            all_problems += p
        for x in csv_targets:
            text = x.read_text(encoding="utf-8")
            if ",=" not in text and not text.startswith("="):
                continue
            f, n, p = scan(x, recalc(x, tmp, csv_in=True), csv_mode=True)
            print(f"[csv ] {x.relative_to(ROOT)}: {f} formulas recalculated, {len(p)} problems")
            total_f += f
            all_problems += p
    for p in all_problems:
        print("  FAIL", p)
    print(f"TOTAL formulas verified: {total_f}; problems: {len(all_problems)}")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main())
