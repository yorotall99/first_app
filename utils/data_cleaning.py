import pandas as pd
import numpy as np
import re


def clean_data(df):
    df = df.copy()

    # 1. Liste des colonnes attendues comme numériques
    cols_numeriques = ['Prix Unitaire (CFA)', 'Quantité', 'Taux Remise', 'Montant (CFA)']

    for col in df.columns:
        # Nettoyage des espaces pour toutes les colonnes
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()

        # Si la colonne est dans notre liste cible, on force le nettoyage
        if col in cols_numeriques:
            # On enlève tout sauf les chiffres, le point et la virgule
            df[col] = df[col].apply(lambda x: re.sub(r'[^\d.,-]', '', str(x)) if x != 'nan' else '0')
            df[col] = df[col].str.replace(',', '.')
            # Conversion forcée, les erreurs deviennent NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. Remplissage des valeurs vides (C'est ici que ça plantait)
    for col in df.columns:
        # On vérifie si la colonne est numérique (float ou int)
        if pd.api.types.is_numeric_dtype(df[col]):
            # On ne calcule la moyenne que s'il y a au moins un chiffre valide
            if df[col].notna().any():
                valeur_moyenne = df[col].mean()
                df[col] = df[col].fillna(valeur_moyenne)
            else:
                # Si toute la colonne est vide, on met 0
                df[col] = df[col].fillna(0)
        else:
            # Pour les colonnes texte
            df[col] = df[col].fillna("Inconnu")

    # 3. Suppression des doublons
    df = df.drop_duplicates()

    return df