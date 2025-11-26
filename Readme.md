# FACS-Data-Export-Pipeline
A Python tool for batch-converting FCS flow cytometry files into TXT or CSV. Supports recursive folder processing and an optional summary mode that generates combined FSC-A and SSC-A tables for quick comparison across samples.

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
