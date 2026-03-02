import pandas as pd
import numpy as np


def clean_data(df, impute_method="median", iqr_threshold=1.5, force_int=True):
    stats = {
        'prev_rows': len(df),
        'cols': len(df.columns),
        'nulls': int(df.isna().sum().sum()),
        'dups': int(df.duplicated().sum()),
        'outliers': 0
    }

    # 1. Suppression des doublons
    df = df.drop_duplicates().copy()

    # 2. Séparation des colonnes
    num_cols = df.select_dtypes(include=[np.number]).columns
    obj_cols = df.select_dtypes(exclude=[np.number]).columns

    # 3. Traitement des numériques (Vectorisé pour la vitesse)
    for col in num_cols:
        # Détection Outliers (IQR)
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - iqr_threshold * IQR
        upper = Q3 + iqr_threshold * IQR

        stats['outliers'] += int(((df[col] < lower) | (df[col] > upper)).sum())

        # Imputation
        if impute_method == "mean":
            fill_val = df[col].mean()
        elif impute_method == "zero":
            fill_val = 0
        else:
            fill_val = df[col].median()

        df[col] = df[col].fillna(fill_val)

        # Casting Int pour IDs et comptages
        if force_int and any(x in col.upper() for x in ["PID", "NUM", "BED", "BATH"]):
            df[col] = df[col].replace([np.inf, -np.inf], 0).fillna(0).astype(np.int64)

    # 4. Traitement du texte
    df[obj_cols] = df[obj_cols].astype(str).apply(lambda x: x.str.strip().replace(['nan', 'NaN', 'None'], 'Inconnu'))

    stats['rows'] = len(df)
    return df, stats