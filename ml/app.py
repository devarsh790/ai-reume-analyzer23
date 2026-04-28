from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running. Send POST requests to /analyze"})

import re

def extract_skills(text):
    skills = [
        "python", "java", "react", "node", "javascript", "typescript", "c++", "c#", "ruby", "php", "go", "rust", "swift", "kotlin", 
        "sql", "mysql", "postgresql", "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp", "git", "linux", "html", "css", 
        "machine learning", "deep learning", "data science", "artificial intelligence", "nlp", "computer vision", "tensorflow", "pytorch", 
        "scikit-learn", "pandas", "numpy", "flask", "django", "fastapi", "express", "spring boot", "angular", "vue", "next.js", "tailwind", 
        "graphql", "rest api", "ci/cd", "agile", "scrum", "ai", "ml", "ui", "ux", "c", "r"
    ]
    
    # Replace punctuation (except + # - .) with spaces to allow exact word matching
    clean_text = re.sub(r'[^\w\s\+\#\-\.]', ' ', text.lower())
    clean_text = f" {clean_text} "
    
    return [skill for skill in skills if f" {skill} " in clean_text]

@app.route("/analyze", methods=["POST"])
def analyze():
    import traceback
    try:
        data = request.get_json(force=True, silent=True) or {}
        resume = data.get("resume_text", "") or ""

        skills_found = extract_skills(resume)
        
        score = 0
        strengths = []
        suggestions = []

        words = resume.split()
        if len(words) < 150:
            suggestions.append("Your resume is quite short. Add more details about your responsibilities and achievements.")
            score += 5
        elif len(words) > 800:
            suggestions.append("Your resume might be too long. Keep it concise and relevant.")
            score += 10
        else:
            strengths.append("Resume length is optimal.")
            score += 20

        lower_resume = resume.lower()
        has_education = "education" in lower_resume or "university" in lower_resume or "degree" in lower_resume
        has_experience = "experience" in lower_resume or "employment" in lower_resume or "work history" in lower_resume
        has_projects = "project" in lower_resume
        
        if has_education:
            score += 15
        else:
            suggestions.append("Consider adding a clear 'Education' section.")
            
        if has_experience:
            score += 20
            strengths.append("Work experience section found.")
        else:
            suggestions.append("Add a 'Work Experience' section detailing your past roles.")
            
        if has_projects:
            score += 15
        else:
            suggestions.append("Adding a 'Projects' section can help showcase your practical skills.")

        doc = nlp(resume)
        metrics_count = sum(1 for ent in doc.ents if ent.label_ in ['PERCENT', 'MONEY', 'CARDINAL'])
        
        if metrics_count > 3:
            strengths.append(f"Great job quantifying your impact! Found {metrics_count} metrics.")
            score += 20
        elif metrics_count > 0:
            strengths.append("Found some quantified metrics.")
            suggestions.append("Try to add even more numbers to quantify your achievements.")
            score += 10
        else:
            suggestions.append("Your resume lacks quantifiable metrics. Add numbers to show the scale of your impact.")

        if len(skills_found) > 5:
            strengths.append(f"Strong technical skills profile ({len(skills_found)} skills detected).")
            score += 10
        elif len(skills_found) > 0:
            score += 5
        else:
            suggestions.append("Include more industry-relevant keywords and skills.")

        score = min(score, 100)
        if len(resume.strip()) == 0:
            score = 0
            suggestions = ["No text could be extracted from your resume. Please try a different PDF format."]
            strengths = []

        return jsonify({
            "score": score,
            "skills": list(set(skills_found)),
            "strengths": strengths,
            "suggestions": suggestions
        })
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(port=8000)