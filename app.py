from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from utils.data_cleaning import clean_data

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    cleaned_df = clean_data(df)

    output_path = os.path.join(OUTPUT_FOLDER, "cleaned_data.csv")
    cleaned_df.to_csv(output_path, index=False)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
