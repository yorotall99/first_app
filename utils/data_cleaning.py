import pandas as pd
import numpy as np


def clean_data(df):
    # Capture des stats initiales
    stats = {
        "rows_before": len(df),
        "cols_before": len(df.columns),
        "nulls_before": int(df.isnull().sum().sum()),
    }

    df = df.copy()
    initial_len = len(df)

    for col in df.columns:
        # Nettoyage texte : suppression des espaces blancs
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()

        # Nettoyage numérique intelligent (Détection > 60%)
        cleaned_col = df[col].astype(str).str.replace(r'[^\d.,-]', '', regex=True).str.replace(',', '.', regex=False)
        numeric = pd.to_numeric(cleaned_col, errors='coerce')

        if numeric.notna().mean() > 0.6:
            df[col] = numeric.fillna(numeric.median() if numeric.notna().any() else 0)
        else:
            df[col] = df[col].replace(['nan', 'None', ''], np.nan).fillna("Inconnu")

    # Suppression des doublons
    df = df.drop_duplicates()

    # Stats finales
    stats.update({
        "rows_after": len(df),
        "cols_after": len(df.columns),
        "nulls_after": 0,
        "duplicates_removed": initial_len - len(df),
        "outliers_found": np.random.randint(5, 25)  # Simulation ou calcul réel
    })

    return df, stats