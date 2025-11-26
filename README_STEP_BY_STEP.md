# Step-by-Step Usage Guide – FCS Batch Export

This guide explains how to use `fcs_batch_export.py` to convert `.fcs` files into TXT/CSV and optionally generate FSC-A/SSC-A summary tables.

---

## 1. Prepare your data

Organize your FCS files in a main folder, with or without subfolders, for example:

```text
D:/Data/FCS_Exports

    /2022-11-17/

        sample_1.fcs

        sample_2.fcs

    2022-11-18/

        sample_3.fcs
```
The script will search recursively, so all subfolders are processed.


## 2. Install Python and dependencies
Make sure you have:

Python 3.8+

pandas

FlowCytometryTools

Install the required packages

bash
```
pip install pandas FlowCytometryTools
```
## 3. Place the script
Put fcs_batch_export.py somewhere convenient, e.g.:
```
D:/Code/fcs-batch-export/fcs_batch_export.py
```
You don’t need to place it inside the data folder; you’ll just point it to your data path.

## 4. Configure the script
Open fcs_batch_export.py in your editor and adjust the user settings at the top:

```
python

## Main directory containing your .fcs files
main_directory = r"D:\Data\FCS_Exports"

## Export mode: "txt", "csv", or "csv_summary"
EXPORT_MODE = "csv_summary"
Export modes
```

Output folder: <original_folder>_converted_to_txt/
```
One tab-separated .txt per .fcs

    csv

    Output folder: <original_folder>_converted_to_csv/

    One comma-separated .csv per .fcs

    csv_summary
```
Same as csv, plus in each folder containing .fcs files:

combined_fsc_a.csv

combined_ssc_a.csv
These contain one column per file (filename without extension) and one row per event.

## 5. Run the script
Open a terminal / command prompt in the folder where fcs_batch_export.py is located, then run:

bash
```
python fcs_batch_export.py
```
The script will:

Walk through main_directory and all subfolders

Find every .fcs file

Create an output folder next to each original folder:
```
.../folder_converted_to_txt/ or

.../folder_converted_to_csv/
```
Export each .fcs file into TXT/CSV

In csv_summary mode, create combined_fsc_a.csv and combined_ssc_a.csv in each folder that contained .fcs files (if FSC-A / SSC-A columns exist).

You’ll see progress messages like:
```
[INFO] Processing directory: D:\Data\FCS_Exports\2022-11-17
[INFO] Saved: D:\Data\FCS_Exports\2022-11-17_converted_to_csv\sample_1.csv
[INFO] Saved summary: D:\Data\FCS_Exports\2022-11-17\combined_fsc_a.csv
```
## 6. Inspect the results
Open the generated files in your tool of choice:

Excel / LibreOffice Calc

R or Python (pandas)

GraphPad, Prism, etc.

The per-file exports contain the full event table for each sample.
The summary files (combined_fsc_a.csv, combined_ssc_a.csv) are convenient for quick comparisons across samples.

## 7. Notes and troubleshooting
If a folder has no .fcs files, it is simply skipped.

If a file doesn’t contain FSC-A or SSC-A, that file is omitted from the corresponding summary table.

The script does not perform gating, compensation, or transformations. It exports exactly what FlowCytometryTools reads from the .fcs files.
