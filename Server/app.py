from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def analyze_cv(cv_text):
    # This is a placeholder for the AI model integration
    # In a real scenario, you would send this text to your AI model (Claude, GPT, etc.)
    # and receive a structured response
    analyzed_data = {
        "skills": ["Python", "Flask", "AI"],
        "experience": "5 years",
        "education": "Bachelor's in Computer Science"
    }
    return analyzed_data

def match_jobs(user_profile):
    # This is a placeholder for job matching logic
    # In a real scenario, you would query your job database and use more sophisticated matching
    job_listings = [
        {"title": "Python Developer", "description": "We need a Python expert..."},
        {"title": "AI Engineer", "description": "Looking for AI enthusiasts..."},
        {"title": "Full Stack Developer", "description": "Flask and React knowledge required..."}
    ]
    
    # Simple matching based on skills
    user_skills = set(user_profile['skills'])
    matched_jobs = []
    for job in job_listings:
        if any(skill.lower() in job['description'].lower() for skill in user_skills):
            matched_jobs.append(job)
    
    return matched_jobs

@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from PDF
        cv_text = extract_text_from_pdf(file_path)
        
        # Analyze CV
        user_profile = analyze_cv(cv_text)
        
        # Match jobs
        recommended_jobs = match_jobs(user_profile)
        
        return jsonify({
            "message": "CV uploaded and analyzed successfully",
            "user_profile": user_profile,
            "recommended_jobs": recommended_jobs
        }), 200
    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)