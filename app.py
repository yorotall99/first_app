from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
import sqlite3
import numpy as np
from datetime import datetime
from utils.data_cleaning import clean_data

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('history.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, date TEXT, 
                  rows_in INTEGER, rows_out INTEGER, dups INTEGER, outliers INTEGER)''')
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    impute_method = request.form.get("impute_method", "median")
    iqr_val = float(request.form.get("iqr_threshold", 1.5))
    force_int = request.form.get("force_int") == "true"

    if not file: return jsonify({"error": "Fichier absent"}), 400

    df = pd.read_excel(file) if file.filename.endswith(('.xlsx', '.xls')) else pd.read_csv(file)

    # Nettoyage
    cleaned_df, stats = clean_data(df, impute_method, iqr_val, force_int)

    # Historique
    conn = sqlite3.connect('history.db')
    conn.execute("INSERT INTO history (filename, date, rows_in, rows_out, dups, outliers) VALUES (?,?,?,?,?,?)",
                 (file.filename, datetime.now().strftime("%d/%m/%Y %H:%M"),
                  stats['prev_rows'], stats['rows'], stats['dups'], stats['outliers']))
    conn.commit()
    conn.close()

    # Preview Top 5
    preview = cleaned_df.head(5).replace({np.nan: None}).to_dict(orient='records')

    # Save
    output_path = "outputs/NEXUS_CLEANED.xlsx"
    os.makedirs("outputs", exist_ok=True)
    cleaned_df.to_excel(output_path, index=False)

    return jsonify({"stats": stats, "preview": preview})


@app.route("/download")
def download():
    return send_file("outputs/NEXUS_CLEANED.xlsx", as_attachment=True)


@app.route("/history")
def get_history():
    conn = sqlite3.connect('history.db')
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    return jsonify({"history": [dict(r) for r in rows]})


if __name__ == "__main__":
    app.run(debug=True)