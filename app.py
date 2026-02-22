from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
import sqlite3
from datetime import datetime
from utils.data_cleaning import clean_data

app = Flask(__name__)


# Initialisation de la base de données pour l'historique
def init_db():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  filename TEXT,
                  date TEXT,
                  rows_in INTEGER,
                  rows_out INTEGER,
                  dups INTEGER,
                  outliers INTEGER)''')
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file: return "Source vide", 400

    # Lecture universelle (Excel ou CSV)
    if file.filename.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    # Nettoyage structuré (utilise Numpy via utils/data_cleaning.py)
    cleaned_df, stats = clean_data(df)

    # SAUVEGARDE DANS L'HISTORIQUE (SQLite)
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (filename, date, rows_in, rows_out, dups, outliers) VALUES (?, ?, ?, ?, ?, ?)",
              (file.filename, datetime.now().strftime("%d/%m/%Y %H:%M"),
               stats['prev_rows'], stats['rows'], stats['dups'], stats['outliers']))
    conn.commit()
    conn.close()

    # GÉNÉRATION DU FICHIER EXCEL (.xlsx)
    output_path = "outputs/NEXUS_CLEANED_FINAL.xlsx"
    os.makedirs("outputs", exist_ok=True)
    cleaned_df.to_excel(output_path, index=False, engine='openpyxl')

    response = send_file(output_path, as_attachment=True)

    # Headers pour le Dashboard JavaScript
    response.headers["X-Stats-Rows"] = str(stats['rows'])
    response.headers["X-Stats-Prev-Rows"] = str(stats['prev_rows'])
    response.headers["X-Stats-Cols"] = str(stats['cols'])
    response.headers["X-Stats-Dups"] = str(stats['dups'])
    response.headers["X-Stats-Nulls"] = str(stats['nulls'])
    response.headers["X-Stats-Outliers"] = str(stats['outliers'])
    response.headers["Access-Control-Expose-Headers"] = "*"

    return response


@app.route("/history")
def get_history():
    conn = sqlite3.connect('history.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({"history": [dict(r) for r in rows]})


if __name__ == "__main__":
    app.run(debug=True)