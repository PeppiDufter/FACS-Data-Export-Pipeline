# FCS Batch Export

A small Python tool to batch-convert Flow Cytometry Standard (`.fcs`) files into TXT or CSV, with an optional summary mode that aggregates FSC-A and SSC-A across all files in each folder.

The script recursively scans a root directory, processes all `.fcs` files it finds, and saves the exports into dedicated output folders next to the original data.

---

## Features

- 🔁 Recursively process all `.fcs` files in a folder tree  
- 📄 Export full event tables to:
  - Tab-separated `.txt`, or
  - Comma-separated `.csv`
- 📊 Optional summary mode:
  - One `.csv` per `.fcs` file
  - Plus per-folder summary files:
    - `combined_fsc_a.csv`
    - `combined_ssc_a.csv`

These summaries have one column per file (column name = filename without extension) and one row per event.

---

## Requirements

- Python 3.8+
- [pandas](https://pandas.pydata.org/)
- [FlowCytometryTools](https://github.com/eyurtsev/FlowCytometryTools)

Install dependencies, for example:

```bash
pip install pandas FlowCytometryTools
