ROLE_SKILLS = {

    "data scientist": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "statistics",
        "sql",
        "scikit-learn"
    ],

    "data analyst": [
        "python",
        "sql",
        "pandas",
        "excel",
        "data visualization",
        "statistics",
        "power bi",
        "tableau"
    ],

    "ml engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn"
    ],

    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "next.js",
        "typescript",
        "git"
    ],

    "backend developer": [
        "python",
        "java",
        "node.js",
        "express",
        "django",
        "flask",
        "sql",
        "mysql",
        "postgresql",
        "api",
        "git"
    ],

    "full stack developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "express",
        "mongodb",
        "sql",
        "git"
    ],

    "devops engineer": [
        "docker",
        "kubernetes",
        "aws",
        "linux",
        "git",
        "ci cd",
        "jenkins",
        "terraform"
    ],

    "software engineer": [
        "python",
        "java",
        "c++",
        "data structures",
        "algorithms",
        "git",
        "sql"
    ]

}

def find_skill_gap(user_skills, role):

    role = role.lower()

    required_skills = ROLE_SKILLS.get(role, [])

    user_skills_lower = [skill.lower().strip() for skill in user_skills]

    matched = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in user_skills_lower:
            matched.append(skill)
        else:
            missing_skills.append(skill)

    score = 0
    if required_skills:
        score = int((len(matched) / len(required_skills)) * 100)

    return {
        "role": role,
        "required_skills": required_skills,
        "user_skills": user_skills,
        "matched_skills": matched,
        "missing_skills": missing_skills,
        "score": score
    }