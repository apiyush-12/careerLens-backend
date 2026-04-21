from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
import traceback

# ==============================
# Load environment variables
# ==============================
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase URL or Key not found in .env file")

# ==============================
# Create Supabase client
# ==============================
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==============================
# NLP Imports
# ==============================
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from skill_gap import find_skill_gap

# ==============================
# Flask Setup
# ==============================
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==============================
# Test Route
# ==============================
@app.route("/")
def home():
    return jsonify({"message": "Backend running successfully"})


# ==============================
# Resume Upload API
# ==============================
@app.route("/resume/upload", methods=["POST"])
def upload_resume():

    try:
        print("\nUpload request received")

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        # Unique filename
        unique_filename = str(uuid.uuid4()) + "_" + file.filename

        # Save locally
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)

        print("File saved locally:", filepath)

        # ==============================
        # Upload to Supabase Storage
        # ==============================
        try:
            with open(filepath, "rb") as f:
                supabase.storage.from_("resumes").upload(
                    unique_filename,
                    f,
                    {"content-type": "application/pdf"}
                )
            print("File uploaded to Supabase")

        except Exception as upload_error:
            print("Upload warning:", upload_error)

        # ==============================
        # NLP Processing (SAFE)
        # ==============================

        resume_text = extract_text_from_pdf(filepath)

        # 🔥 Handle empty text
        if not resume_text or len(resume_text.strip()) == 0:
            print("WARNING: No text extracted from resume")

            return jsonify({
                "error": "Could not extract text from resume (PDF may be scanned or unsupported)"
            }), 400

        print("TEXT LENGTH:", len(resume_text))
        print("TEXT SAMPLE:", resume_text[:200])

        # 🔥 Safe skill extraction
        try:
            skills = extract_skills(resume_text)
        except Exception as skill_error:
            print("Skill extraction error:", skill_error)
            skills = []

        print("Extracted skills:", skills)

        # ==============================
        # Save to Supabase Table (SAFE)
        # ==============================

        try:
            response = supabase.table("resume-analysis").insert({
                "file_name": unique_filename,
                "extracted_skills": list(skills)
            }).execute()

            print("DB INSERT SUCCESS:", response)

        except Exception as db_error:
            print("DB ERROR:", db_error)

        return jsonify({
            "message": "Resume uploaded successfully",
            "skills": skills
        })

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ==============================
# Resume History API
# ==============================
@app.route("/resume/history", methods=["GET"])
def resume_history():

    try:
        response = supabase.table("resume-analysis") \
            .select("*") \
            .order("created_at", desc=True) \
            .execute()

        return jsonify(response.data)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ==============================
# Skill Gap API
# ==============================
@app.route("/skill-gap", methods=["POST"])
def skill_gap():

    try:
        data = request.json

        user_skills = data.get("skills", [])
        role = data.get("role")

        if not role:
            role = "data scientist"

        print("User skills:", user_skills)
        print("Target role:", role)

        result = find_skill_gap(user_skills, role)

        return jsonify(result)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "required_skills": []
        })


# ==============================
# Career Roles API
# ==============================
@app.route("/roles", methods=["GET"])
def get_roles():

    roles = [
        "data scientist",
        "frontend developer",
        "backend developer",
        "devops engineer",
        "machine learning engineer",
        "data analyst",
        "ai engineer"
    ]

    return jsonify(roles)


# ==============================
# Skills API (UPDATED ✅)
# ==============================

@app.route("/skills", methods=["GET"])
def get_skills():
    try:
        response = supabase.table("user-skills") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        if response.data:
            return jsonify({"skills": response.data[0]["skills"]})

        return jsonify({"skills": []})

    except Exception as e:
        print("ERROR (GET SKILLS):", str(e))
        return jsonify({"skills": []})


@app.route("/skills", methods=["POST"])
def save_skills():
    try:
        data = request.json
        skills = data.get("skills", [])

        print("Saving skills:", skills)

        supabase.table("user-skills").insert({
            "skills": skills
        }).execute()

        return jsonify({"message": "Skills saved successfully"})

    except Exception as e:
        print("ERROR (SAVE SKILLS):", str(e))
        return jsonify({"error": str(e)}), 500
    

@app.route("/roadmap", methods=["POST"])
def roadmap():
    data = request.json

    missing_skills = data.get("missing_skills", [])

    roadmap = []

    for i, skill in enumerate(missing_skills):
        roadmap.append({
            "id": f"node-{i}",
            "title": skill,
            "description": f"Learn {skill} in depth",
            "phase": 1 if i < len(missing_skills)/2 else 2
        })

    return jsonify({"nodes": roadmap})


# ==============================
# Run Server
# ==============================
if __name__ == "__main__":
    print("\nStarting Flask server...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
