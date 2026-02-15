import pandas as pd
import numpy as np
import re

def is_numeric_like(series):
    cleaned = series.astype(str).str.replace(r'[^\d.,-]', '', regex=True).str.replace(',', '.', regex=False)
    numeric = pd.to_numeric(cleaned, errors='coerce')
    return numeric.notna().mean() > 0.6  # 60% de chiffres → colonne numérique

def clean_data(df):
    df = df.copy()

    for col in df.columns:
        # Nettoyage texte
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()

        # Colonnes numériques détectées automatiquement
        if is_numeric_like(df[col]):
            df[col] = df[col].astype(str).str.replace(r'[^\d.,-]', '', regex=True).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median() if df[col].notna().any() else 0)
        else:
            df[col] = df[col].replace(['nan', 'None', ''], np.nan)
            df[col] = df[col].fillna("Inconnu")

    df = df.drop_duplicates()
    return df
