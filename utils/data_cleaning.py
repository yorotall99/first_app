import pandas as pd
import numpy as np


def clean_data(df):
    stats = {
        'prev_rows': len(df),
        'cols': len(df.columns),
        'nulls': int(df.isna().sum().sum()),
        'dups': int(df.duplicated().sum()),
        'outliers': 0
    }

    # 1. Suppression des doublons
    df = df.drop_duplicates().copy()

    for col in df.columns:
        col_upper = col.upper()

        # --- STRUCTURE DES IDENTIFIANTS (PID, ST_NUM) ---
        if any(x in col_upper for x in ["PID", "NUM"]):
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            df[col] = df[col].astype(np.int64)  # Force l'entier (plus de .0)

        # --- STRUCTURE DES COMPTAGES ET SURFACES ---
        elif any(x in col_upper for x in ["BED", "BATH", "SQ", "FT"]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            median_val = df[col].median() if not df[col].isna().all() else 0
            df[col] = df[col].fillna(round(median_val)).astype(np.int64)

        # --- STRUCTURE DU TEXTE ---
        else:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(['nan', 'None', '', '12', '--'], "Inconnu")

    stats['rows'] = len(df)
    return df, stats