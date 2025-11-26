# FCS Batch Export

Small utility script to batch-convert Flow Cytometry Standard (`.fcs`) files into text-based tables (TXT / CSV) and optionally generate simple summary tables for key channels.

The script recursively scans a root directory, processes all `.fcs` files it finds, and writes the outputs next to the original data in clearly named folders.

## Features

- 🔍 Recursively walks through a root folder and its subfolders
- 📄 Per-file export of full event tables to:
  - Tab-separated `.txt`, or
  - Comma-separated `.csv`
- 📊 Optional summary mode:
  - One `.csv` per `.fcs` file
  - Plus per-folder summary tables:
    - `combined_fsc_a.csv` (columns = files, rows = events for FSC-A)
    - `combined_ssc_a.csv` (columns = files, rows = events for SSC-A)

This is useful if you want quick access to raw FCS data in Excel, R, Python, or GraphPad, and/or perform simple comparisons across samples using FSC-A and SSC-A.

## Requirements

- Python 3.8+
- [pandas](https://pandas.pydata.org/)
- [FlowCytometryTools](https://github.com/eyurtsev/FlowCytometryTools)

Install dependencies, for example:

```bash
pip install pandas FlowCytometryTools
