from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import csv
from utils.data_cleaning import clean_data

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def load_any_file(filepath, filename):
    ext = filename.lower().split('.')[-1]

    try:
        if ext in ['xlsx', 'xls']:
            return pd.read_excel(filepath)
        else:
            # Tous les autres fichiers : tentative CSV
            try:
                return pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8')
            except:
                return pd.read_csv(filepath, sep=None, engine='python', encoding='latin-1', quoting=csv.QUOTE_NONE)
    except Exception as e:
        raise ValueError("Le fichier n'est pas un fichier de données lisible.") from e


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "Erreur : Aucun fichier", 400

    file = request.files["file"]
    if file.filename == '':
        return "Erreur : Nom vide", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        print(f"--- Analyse du fichier : {file.filename} ---")

        df = load_any_file(filepath, file.filename)

        print(f"Colonnes lues : {df.columns.tolist()}")

        # NETTOYAGE
        print("Démarrage du nettoyage...")
        cleaned_df = clean_data(df)
        print("Nettoyage réussi.")

        # SAUVEGARDE
        output_path = os.path.join(OUTPUT_FOLDER, "cleaned_data.csv")
        cleaned_df.to_csv(output_path, index=False, encoding='utf-8')

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"!!! ERREUR SERVEUR : {str(e)}")
        return f"Erreur lors du traitement : {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
