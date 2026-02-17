from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
from utils.data_cleaning import clean_data

app = Flask(__name__)
UPLOAD_FOLDER, OUTPUT_FOLDER = "uploads", "outputs"
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'json', 'xml'}

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

def load_any_file(filepath, filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['xlsx', 'xls']: return pd.read_excel(filepath)
    if ext == 'json': return pd.read_json(filepath)
    if ext == 'xml': return pd.read_xml(filepath)
    return pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file: return jsonify({"error": "Aucun fichier"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        df = load_any_file(filepath, file.filename)
        cleaned_df, stats = clean_data(df)

        output_name = f"nexus_cleaned_{file.filename.split('.')[0]}.csv"
        cleaned_df.to_csv(os.path.join(OUTPUT_FOLDER, output_name), index=False)

        return jsonify({"status": "success", "stats": stats, "filename": output_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)