from flask import Flask, request, send_file
import os
import tempfile
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return 'PDF Compressor API is running!'

@app.route('/compress', methods=['POST'])
def compress_pdf():
    if 'file' not in request.files:
        return {'error': 'No file uploaded'}, 400

    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return {'error': 'Only PDF files are supported'}, 400

    quality = request.form.get('quality', '50')
    try:
        quality = int(quality)
        quality = max(10, min(quality, 100))
    except:
        quality = 50

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, 'input.pdf')
        output_path = os.path.join(tmpdir, 'output.pdf')
        file.save(input_path)

        if quality < 30:
            setting = '/screen'
        elif quality < 60:
            setting = '/ebook'
        elif quality < 85:
            setting = '/printer'
        else:
            setting = '/prepress'

        try:
            subprocess.run([
                'gs',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={setting}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-sOutputFile={output_path}',
                input_path
            ], check=True)

            return send_file(output_path, as_attachment=True, download_name='compressed.pdf')
        except subprocess.CalledProcessError:
            return {'error': 'Compression failed'}, 500

if __name__ == '__main__':
    app.run(debug=True)
