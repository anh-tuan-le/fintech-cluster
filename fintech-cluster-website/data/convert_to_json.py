#!/usr/bin/env python3
"""
convert_to_json.py
==================
Convert a CSV / XLSX / XLS / TXT / TSV file of dated index values into the
JSON format used by the Indices page:  [[timestamp_ms, value], ...]

The Indices charts (data/defi_tvl.json, etc.) expect each point as
[unix_timestamp_in_milliseconds, numeric_value], sorted oldest -> newest.
This script does that conversion for you.

--------------------------------------------------------------------------
QUICK START
--------------------------------------------------------------------------
1. Put your data file anywhere (e.g. data/my_index.csv). It needs two
   columns: a DATE column and a VALUE column. Example CSV:

        date,value
        2024-01-01,100.0
        2024-02-01,102.4
        2024-03-01,98.7

2. Install dependencies once (only needed for Excel files):

        pip install pandas openpyxl

3. Run it:

        python convert_to_json.py my_index.csv

   -> writes my_index.json next to it.

   Choose the output name explicitly:

        python convert_to_json.py my_index.csv -o defi_tvl.json

   Pick columns by name if they aren't auto-detected:

        python convert_to_json.py raw.xlsx --date-col Month --value-col TVL

4. Copy/commit the resulting .json into the data/ folder and refresh the site.

--------------------------------------------------------------------------
SUPPORTED INPUTS
--------------------------------------------------------------------------
  .csv .tsv .txt   -> read directly (delimiter auto-detected)
  .xlsx .xls       -> requires pandas + openpyxl

If you don't pass --date-col / --value-col, the script tries to guess:
  - date column: first column whose name contains "date"/"month"/"time",
    otherwise the first column.
  - value column: first numeric column that isn't the date column.
--------------------------------------------------------------------------
"""

import argparse, csv, json, os, sys
from datetime import datetime

DATE_HINTS  = ("date", "month", "time", "period", "day")
VALUE_HINTS = ("value", "index", "price", "tvl", "amount", "level", "close")

DATE_FORMATS = [
    "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y",
    "%Y-%m", "%Y/%m", "%b %Y", "%B %Y", "%d-%b-%Y",
    "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y",
]

def parse_date(s):
    s = str(s).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # last resort: let datetime try ISO
    try:
        return datetime.fromisoformat(s)
    except Exception:
        raise ValueError(f"Could not parse date: '{s}'. "
                         f"Use a format like 2024-01-01.")

def to_ms(dt):
    return int(dt.timestamp() * 1000)

def clean_number(x):
    if x is None:
        return None
    s = str(x).strip().replace(",", "").replace("$", "").replace("%", "")
    if s == "" or s.lower() in ("na", "nan", "null", "none"):
        return None
    return float(s)

def read_tabular(path):
    """Return (headers, rows) for csv/txt/tsv/xlsx/xls."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        try:
            import pandas as pd
        except ImportError:
            sys.exit("Excel files need pandas + openpyxl.\n"
                     "  pip install pandas openpyxl")
        df = pd.read_excel(path)
        headers = [str(c) for c in df.columns]
        rows = df.astype(object).where(df.notna(), None).values.tolist()
        return headers, rows
    # text formats
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel  # default to comma
        reader = csv.reader(f, dialect)
        rows = [r for r in reader if any(str(c).strip() for c in r)]
    if not rows:
        sys.exit("File appears to be empty.")
    headers = [h.strip() for h in rows[0]]
    return headers, rows[1:]

def pick_column(headers, hints, explicit, exclude=None):
    if explicit:
        if explicit in headers:
            return headers.index(explicit)
        sys.exit(f"Column '{explicit}' not found. Available: {headers}")
    for i, h in enumerate(headers):
        if exclude is not None and i == exclude:
            continue
        if any(hint in h.lower() for hint in hints):
            return i
    return None

def main():
    ap = argparse.ArgumentParser(
        description="Convert CSV/XLSX/TXT to [[timestamp_ms, value], ...] JSON "
                    "for the FinTech Indices page.")
    ap.add_argument("input", help="Path to .csv/.tsv/.txt/.xlsx/.xls file")
    ap.add_argument("-o", "--output", help="Output .json path "
                    "(default: same name as input with .json)")
    ap.add_argument("--date-col", help="Name of the date column")
    ap.add_argument("--value-col", help="Name of the value column")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"Input not found: {args.input}")

    headers, rows = read_tabular(args.input)

    di = pick_column(headers, DATE_HINTS, args.date_col)
    if di is None:
        di = 0  # fall back to first column
    vi = pick_column(headers, VALUE_HINTS, args.value_col, exclude=di)
    if vi is None:
        # first column that parses as a number and isn't the date col
        for i in range(len(headers)):
            if i == di:
                continue
            for r in rows:
                if i < len(r) and clean_number(r[i]) is not None:
                    vi = i
                    break
            if vi is not None:
                break
    if vi is None:
        sys.exit(f"Could not find a numeric value column. Headers: {headers}\n"
                 f"Try --value-col <name>.")

    print(f"Date column : '{headers[di]}'  (index {di})")
    print(f"Value column: '{headers[vi]}'  (index {vi})")

    out, skipped = [], 0
    for r in rows:
        if di >= len(r) or vi >= len(r):
            skipped += 1; continue
        val = clean_number(r[vi])
        if val is None:
            skipped += 1; continue
        try:
            dt = parse_date(r[di])
        except ValueError as e:
            print("  skip:", e); skipped += 1; continue
        out.append([to_ms(dt), round(val, 4)])

    out.sort(key=lambda p: p[0])

    if not out:
        sys.exit("No valid rows converted. Check your columns/date format.")

    output = args.output or (os.path.splitext(args.input)[0] + ".json")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"\nWrote {len(out)} points -> {output}"
          + (f"  ({skipped} rows skipped)" if skipped else ""))
    print("Now copy this file into the data/ folder (if it isn't already) "
          "and refresh the Indices page.")

if __name__ == "__main__":
    main()
