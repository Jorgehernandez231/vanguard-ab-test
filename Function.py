import pandas as pd
import numpy as np

 # Basic Data Cleaning Function
 

def basic_data_cleaning(
    df, 
    drop_missing: bool=False, 
    fill_missing=None,         # scalar, dict, or Series are supported
    remove_outliers: bool=False,
    drop_duplicates_subset=None, 
    show_missing_rows: bool=True, 
    show_info: bool=True,
    verbose: bool=True
):
    """
    Perform basic data cleaning steps on a pandas DataFrame and print a detailed cleaning report,
    including a per-column missing-values summary (before vs after) and the action taken.

    Parameters
    ----------
    df : pd.DataFrame
    drop_missing : bool
        Drop any rows containing at least one NaN.
    fill_missing : scalar | dict | pd.Series | None
        Value(s) to fill NaNs with. If dict/Series, applied per column.
    remove_outliers : bool
        Remove outliers from numeric columns via IQR rule.
    show_missing_rows : bool
        Print the subset of rows that contain any NaN (before cleaning).
    show_info : bool
        Print df.info() before and after cleaning.
    verbose : bool
        Print reports.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """

    # Snapshot BEFORE
    initial_shape = df.shape
    if show_info:
        print("\n" + "="*70)
        print(" 📝 DATAFRAME INFO BEFORE CLEANING ")
        print("="*70)
        df.info()
        print("="*70)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # ----- Handle duplicates -----
    if drop_duplicates_subset:
        # Show preview of duplicates before dropping
        duplicates_preview = df[df.duplicated(subset=drop_duplicates_subset, keep=False)]
        duplicates_count = df.duplicated(subset=drop_duplicates_subset).sum()
        if verbose and duplicates_count > 0:
            print(f"\n🔍 Found {duplicates_count} duplicate rows based on {drop_duplicates_subset!r}:")
            print(duplicates_preview.head(5))  # Show first 5 duplicates
        df = df.drop_duplicates(subset=drop_duplicates_subset, keep="first")
        duplicates_removed = duplicates_count
    else:
        duplicates_count = df.duplicated().sum()
        df = df.drop_duplicates()
        duplicates_removed = duplicates_count

    # Strip whitespace in string columns
    obj_cols = df.select_dtypes(include=['object']).columns.tolist()
    trimmed_cols = []
    for col in obj_cols:
        # Detect any leading/trailing whitespace in this column
        # (safe even if column has NaNs)
        s = df[col].astype("string")  # preserves NaN but allows .str ops
        if s.str.match(r"^\s+").fillna(False).any() or s.str.match(r".*\s+$").fillna(False).any():
            trimmed_cols.append(col)
        df[col] = df[col].astype("string").str.strip()

    # ----- Missing values reporting BEFORE -----
    na_before_series = df.isna().sum()
    na_before_total = int(na_before_series.sum())

    if verbose:
        if na_before_total > 0:
            print("\n📌 Missing Values Summary BEFORE Cleaning:")
            summary_before = (
                na_before_series[na_before_series > 0]
                .sort_values(ascending=False)
                .to_frame(name="Missing Count")
                .assign(Missing_Percent=lambda x: (x["Missing Count"] / len(df) * 100).round(2))
            )
            print(summary_before)
            if show_missing_rows:
                print("-"*70)
                print("🔍 Rows Containing Missing Values:")
                print(df[df.isna().any(axis=1)])
        else:
            print("\n✅ No missing values detected before cleaning.")

    # ----- Handle missing values -----
    if drop_missing:
        df = df.dropna()
        missing_action_global = f"All rows with missing values were removed ({na_before_total} NaNs dropped)."
    elif fill_missing is not None:
        df = df.fillna(fill_missing)
        missing_action_global = f"All NaNs were replaced with: {fill_missing!r}."
    else:
        missing_action_global = f"{na_before_total} missing values remain unfilled."

    # ----- Numeric conversion (safe) -----
    converted_cols = []
    for col in df.columns:
        if df[col].dtype == "object":
            try:
                converted = pd.to_numeric(df[col])
                df[col] = converted
                converted_cols.append(col)
            except (ValueError, TypeError):
                pass

    # ----- Outlier removal (optional) -----
    outliers_removed = 0
    if remove_outliers:
        num_cols = df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            before_rows = len(df)
            df = df[(df[col] >= lower) & (df[col] <= upper)]
            outliers_removed += before_rows - len(df)

    df = df.reset_index(drop=True)

    # ----- Missing values reporting AFTER & per-column actions -----
    na_after_series = df.isna().sum()
    na_after_total = int(na_after_series.sum())

    # Build per-column action description
    actions = {}
    # Normalize fill_missing to decide per-column action text
    fill_is_scalar = np.isscalar(fill_missing) or isinstance(fill_missing, (str, bytes))
    fill_is_map = isinstance(fill_missing, (dict, pd.Series))

    for col in df.columns:
        if drop_missing:
            # If we dropped rows, any column that had NaNs contributed to the drop
            actions[col] = "rows with NaN dropped" if na_before_series.get(col, 0) > 0 else "unchanged"
        elif fill_is_scalar:
            if na_before_series.get(col, 0) > 0:
                actions[col] = f"filled with {repr(fill_missing)}"
            else:
                actions[col] = "unchanged"
        elif fill_is_map:
            if col in fill_missing and na_before_series.get(col, 0) > 0:
                actions[col] = f"filled with {repr(fill_missing[col])}"
            elif na_before_series.get(col, 0) > 0:
                actions[col] = "unchanged (no fill rule for this column)"
            else:
                actions[col] = "unchanged"
        else:
            # no fill, no drop
            actions[col] = "unchanged"

    per_col_report = pd.DataFrame({
        "NaNs Before": na_before_series,
        "NaNs After": na_after_series,
        "Action": pd.Series(actions)
    }).sort_values("NaNs Before", ascending=False)

    # Show df.info() AFTER
    if show_info:
        print("\n" + "="*70)
        print(" 📊 DATAFRAME INFO AFTER CLEANING ")
        print("="*70)
        df.info()
        print("="*70)

    # ----- Print final reports -----
    if verbose:
        print("\n" + "="*70)
        print(" 🧹 FINAL DATA CLEANING SUMMARY ")
        print("="*70)
        print(f"📊 Shape: {initial_shape}  →  {df.shape}")
        print(f"✅ Duplicates removed: {duplicates_removed} (based on: {drop_duplicates_subset or 'all columns'})")
        print(f"✅ Missing values: {na_before_total} → {na_after_total}")
        print(f"   ➝ {missing_action_global}")
        print(f"✅ Trimmed columns: {trimmed_cols if trimmed_cols else 'None'}")
        print(f"✅ Converted to numeric: {converted_cols if converted_cols else 'None'}")
        if remove_outliers:
            print(f"✅ Outlier rows removed: {outliers_removed}")
        print("-"*70)
        print("📑 Per-column missing values report:")
        print(per_col_report)
        print("="*70 + "\n")

    return df