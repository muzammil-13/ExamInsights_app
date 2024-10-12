# app.py
from flask import Flask, render_template, request, jsonify
from exam_analyzer import ExamAnalyzer
import os

app = Flask(__name__)
analyzer = ExamAnalyzer()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_exam_papers():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        results = analyzer.analyze(filename)
        os.remove(filename)  # Clean up the uploaded file
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)