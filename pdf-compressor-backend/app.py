# app.py
from flask import Flask, request, send_file, jsonify
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/compress", methods=["POST"])
def compress_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    pdf_file = request.files['file']
    quality = request.form.get('quality', 'screen')

    input_path = os.path.join(UPLOAD_FOLDER, "input.pdf")
    output_path = os.path.join(UPLOAD_FOLDER, "compressed.pdf")

    pdf_file.save(input_path)

    try:
        command = [
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{quality}",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_path}", input_path
        ]
        subprocess.run(command, check=True)

        return send_file(output_path, mimetype='application/pdf', as_attachment=True, download_name='compressed.pdf')

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Compression failed."}), 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

@app.route("/")
def home():
    return "PDF Compressor Backend Running"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
