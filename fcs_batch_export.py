"""
fcs_batch_export.py

Batch convert Flow Cytometry Standard (.fcs) files into text-based tables.

Features
--------
- Recursively scan a root directory for .fcs files.
- For each .fcs file, export the full event table to:
    - TXT (tab-separated), or
    - CSV (comma-separated).
- Optional summary mode:
    - Creates one CSV per .fcs file.
    - Additionally aggregates FSC-A and SSC-A channels from all .fcs files
      in each directory into:
        - combined_fsc_a.csv
        - combined_ssc_a.csv

Dependencies
------------
- Python 3.8+
- pandas
- FlowCytometryTools

Install dependencies (example):
    pip install pandas FlowCytometryTools
"""

import os
import pandas as pd
from FlowCytometryTools import FCMeasurement


# ============================================================================
# USER SETTINGS
# ============================================================================

#: Main directory containing your .fcs files (subfolders are processed too).
main_directory = r"C:\\\s\Desktop\FCS Exports\4 reps lightswitch"
# Example alternative:
# main_directory = r"C:\\\\Desktop\FCS Exports\light switch PK"

#: Export mode:
#:   "txt"         -> one .txt (tab-separated) file per .fcs
#:   "csv"         -> one .csv (comma-separated) file per .fcs
#:   "csv_summary" -> one .csv per .fcs + per-folder FSC-A / SSC-A summaries
EXPORT_MODE = "csv_summary"  # "txt", "csv", or "csv_summary"


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def convert_fcs(file_path: str, output_folder: str, export_mode: str):
    """
    Load a single .fcs file, export its full data table, and optionally
    return FSC-A and SSC-A columns for summary aggregation.

    Parameters
    ----------
    file_path : str
        Absolute or relative path to the .fcs file.
    output_folder : str
        Folder where the exported table will be written. The folder must
        exist before calling this function.
    export_mode : str
        One of:
            - "txt"         : export as tab-separated .txt
            - "csv"         : export as comma-separated .csv
            - "csv_summary" : export as comma-separated .csv and return
                              FSC-A / SSC-A columns for aggregation.

    Returns
    -------
    (pd.Series | None, pd.Series | None)
        (fsc, ssc) where each is a pandas Series containing the corresponding
        channel data, or None if the column is not present or not needed.

        - For "txt" and "csv" modes, (None, None) is always returned.
        - For "csv_summary" mode, Series are returned if columns exist.
    """
    # Load .fcs using FlowCytometryTools
    sample = FCMeasurement(ID="Sample", datafile=file_path)

    # Convert the underlying data to a pandas DataFrame
    df = sample.data

    # Decide file extension and separator based on the export mode
    if export_mode == "txt":
        ext = ".txt"
        sep = "\t"   # tab-separated text file
    else:
        # For both "csv" and "csv_summary" we export CSV
        ext = ".csv"
        sep = ","    # comma-separated CSV

    # Build a clean output filename with new extension
    base_name = os.path.basename(file_path)
    name_no_ext, _ = os.path.splitext(base_name)
    output_file = os.path.join(output_folder, name_no_ext + ext)

    # Write full event table
    df.to_csv(output_file, index=False, sep=sep)
    print(f"[INFO] Saved: {output_file}")

    # Summary mode: return FSC-A / SSC-A columns (if present)
    if export_mode == "csv_summary":
        fsc = df["FSC-A"] if "FSC-A" in df.columns else None
        ssc = df["SSC-A"] if "SSC-A" in df.columns else None
        return fsc, ssc

    # Other modes: nothing to aggregate
    return None, None


# ============================================================================
# MAIN LOGIC
# ============================================================================

if __name__ == "__main__":
    # Validate export mode early to avoid silent errors
    valid_modes = {"txt", "csv", "csv_summary"}
    if EXPORT_MODE not in valid_modes:
        raise ValueError(
            f"Unknown EXPORT_MODE: {EXPORT_MODE!r}. "
            f"Valid options are: {', '.join(sorted(valid_modes))}"
        )

    # Decide suffix for per-folder output directories
    # This keeps outputs next to the original data but clearly separated.
    if EXPORT_MODE == "txt":
        folder_suffix = "_converted_to_txt"
    else:
        # For both "csv" and "csv_summary"
        folder_suffix = "_converted_to_csv"

    # Walk through the directory tree starting from main_directory
    for dirpath, dirnames, filenames in os.walk(main_directory):
        # Normalize file list once (in case-insensitive fashion)
        fcs_files = [f for f in filenames if f.lower().endswith(".fcs")]
        if not fcs_files:
            # Nothing to do in this directory
            continue

        print(f"\n[INFO] Processing directory: {dirpath}")
        output_folder = dirpath + folder_suffix
        os.makedirs(output_folder, exist_ok=True)

        # ---------------------------------------------------------------------
        # SIMPLE MODES: "txt" or "csv"
        #   -> just convert all .fcs files in this directory.
        # ---------------------------------------------------------------------
        if EXPORT_MODE in {"txt", "csv"}:
            for file in fcs_files:
                file_path = os.path.join(dirpath, file)
                convert_fcs(file_path, output_folder, EXPORT_MODE)

        # ---------------------------------------------------------------------
        # SUMMARY MODE: "csv_summary"
        #   -> per-file CSV + per-directory combined FSC-A / SSC-A tables.
        # ---------------------------------------------------------------------
        elif EXPORT_MODE == "csv_summary":
            # Use dictionaries to collect columns by filename
            all_fsc_a_columns = {}
            all_ssc_a_columns = {}

            # Convert each file and optionally collect FSC-A / SSC-A
            for file in fcs_files:
                file_path = os.path.join(dirpath, file)
                fsc_a_column, ssc_a_column = convert_fcs(
                    file_path, output_folder, EXPORT_MODE
                )

                # Use filename (without extension) as column name
                filename_without_extension, _ = os.path.splitext(file)
                if fsc_a_column is not None:
                    all_fsc_a_columns[filename_without_extension] = fsc_a_column
                if ssc_a_column is not None:
                    all_ssc_a_columns[filename_without_extension] = ssc_a_column

            # After finishing this directory, write the combined summary files
            if all_fsc_a_columns:
                combined_fsc_a_df = pd.DataFrame(all_fsc_a_columns)
                combined_fsc_a_path = os.path.join(dirpath, "combined_fsc_a.csv")
                combined_fsc_a_df.to_csv(combined_fsc_a_path, index=False)
                print(f"[INFO] Saved summary: {combined_fsc_a_path}")

            if all_ssc_a_columns:
                combined_ssc_a_df = pd.DataFrame(all_ssc_a_columns)
                combined_ssc_a_path = os.path.join(dirpath, "combined_ssc_a.csv")
                combined_ssc_a_df.to_csv(combined_ssc_a_path, index=False)
                print(f"[INFO] Saved summary: {combined_ssc_a_path}")
