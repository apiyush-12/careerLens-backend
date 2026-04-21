import re

# Expanded skill dictionary
SKILL_ALIASES = {

    # ── Programming Languages ──────────────────────────────────────────────
    "python":       ["python"],
    "java":         ["java"],
    "c++":          ["c++", "cpp", "c plus plus"],
    "c":            ["c programming", "c language"],
    "c#":           ["c#", "csharp", "c sharp"],
    "r":            ["r programming", "r language"],
    "go":           ["golang", "go language", "go programming"],
    "rust":         ["rust", "rust lang"],
    "scala":        ["scala"],
    "kotlin":       ["kotlin"],
    "swift":        ["swift"],
    "ruby":         ["ruby"],
    "php":          ["php"],
    "perl":         ["perl"],
    "matlab":       ["matlab"],
    "julia":        ["julia"],
    "bash":         ["bash", "shell scripting", "shell script"],
    "typescript":   ["typescript", "ts"],
    "javascript":   ["javascript", "js"],

    # ── Web Frontend ───────────────────────────────────────────────────────
    "html":         ["html", "html5"],
    "css":          ["css", "css3"],
    "sass":         ["sass", "scss"],
    "react":        ["react", "reactjs", "react js"],
    "next.js":      ["next", "nextjs", "next js"],
    "vue.js":       ["vue", "vuejs", "vue js"],
    "angular":      ["angular", "angularjs"],
    "svelte":       ["svelte", "sveltejs"],
    "tailwind css": ["tailwind", "tailwindcss", "tailwind css"],
    "bootstrap":    ["bootstrap"],
    "jquery":       ["jquery"],
    "redux":        ["redux"],
    "graphql":      ["graphql"],
    "webpack":      ["webpack"],

    # ── Web Backend ────────────────────────────────────────────────────────
    "node.js":      ["node", "nodejs", "node js"],
    "express.js":   ["express", "expressjs", "express js"],
    "django":       ["django"],
    "flask":        ["flask"],
    "fastapi":      ["fastapi", "fast api"],
    "spring":       ["spring", "spring boot"],
    "rails":        ["rails", "ruby on rails"],
    "laravel":      ["laravel"],
    "asp.net":      ["asp.net", "aspnet", "asp net"],

    # ── Mobile ─────────────────────────────────────────────────────────────
    "react native": ["react native"],
    "flutter":      ["flutter"],
    "android":      ["android", "android development"],
    "ios":          ["ios", "ios development"],
    "xamarin":      ["xamarin"],

    # ── Data Libraries ─────────────────────────────────────────────────────
    "numpy":        ["numpy"],
    "pandas":       ["pandas"],
    "scikit-learn": ["scikit learn", "scikit-learn", "sklearn"],
    "scipy":        ["scipy"],
    "matplotlib":   ["matplotlib"],
    "seaborn":      ["seaborn"],
    "plotly":       ["plotly"],
    "tensorflow":   ["tensorflow", "tf"],
    "pytorch":      ["pytorch", "torch"],
    "keras":        ["keras"],
    "hugging face": ["hugging face", "huggingface", "transformers"],
    "opencv":       ["opencv", "open cv"],
    "xgboost":      ["xgboost"],
    "lightgbm":     ["lightgbm"],

    # ── Data Science & AI ──────────────────────────────────────────────────
    "machine learning":   ["machine learning", "ml"],
    "deep learning":      ["deep learning", "dl"],
    "nlp":                ["nlp", "natural language processing"],
    "computer vision":    ["computer vision", "cv"],
    "statistics":         ["statistics", "statistical analysis"],
    "data analysis":      ["data analysis", "data analytics"],
    "data engineering":   ["data engineering"],
    "feature engineering":["feature engineering"],
    "time series":        ["time series", "time series analysis"],
    "reinforcement learning": ["reinforcement learning", "rl"],
    "llm":                ["llm", "large language model"],
    "generative ai":      ["generative ai", "gen ai", "genai"],

    # ── Databases ──────────────────────────────────────────────────────────
    "sql":          ["sql", "structured query language", "mysql", "MySQL","SQL"],
    "postgresql":   ["postgresql", "postgres"],
    "sqlite":       ["sqlite"],
    "mongodb":      ["mongodb", "mongo"],
    "redis":        ["redis"],
    "cassandra":    ["cassandra"],
    "elasticsearch":["elasticsearch", "elastic search"],
    "firebase":     ["firebase"],
    "dynamodb":     ["dynamodb", "dynamo db"],
    "oracle":       ["oracle db", "oracle database"],
    "neo4j":        ["neo4j"],
    "snowflake":    ["snowflake"],
    "bigquery":     ["bigquery", "big query"],

    # ── Cloud & DevOps ─────────────────────────────────────────────────────
    "aws":              ["aws", "amazon web services"],
    "azure":            ["azure", "microsoft azure"],
    "gcp":              ["gcp", "google cloud", "google cloud platform"],
    "docker":           ["docker"],
    "kubernetes":       ["kubernetes", "k8s"],
    "terraform":        ["terraform"],
    "ansible":          ["ansible"],
    "jenkins":          ["jenkins"],
    "github actions":   ["github actions"],
    "gitlab ci":        ["gitlab ci", "gitlab cicd"],
    "ci/cd":            ["ci cd", "cicd", "continuous integration", "continuous deployment"],
    "linux":            ["linux", "ubuntu", "debian", "centos"],
    "nginx":            ["nginx"],
    "apache":           ["apache"],

    # ── Tools & Platforms ──────────────────────────────────────────────────
    "git":          ["git"],
    "github":       ["github"],
    "gitlab":       ["gitlab"],
    "jira":         ["jira"],
    "excel":        ["excel", "microsoft excel"],
    "tableau":      ["tableau"],
    "power bi":     ["power bi", "powerbi"],
    "data visualization": ["data visualization", "data viz"],
    "jupyter":      ["jupyter", "jupyter notebook"],
    "airflow":      ["airflow", "apache airflow"],
    "spark":        ["spark", "apache spark", "pyspark"],
    "kafka":        ["kafka", "apache kafka"],
    "hadoop":       ["hadoop"],
    "dbt":          ["dbt", "data build tool"],

    # ── Cybersecurity ──────────────────────────────────────────────────────
    "cybersecurity":    ["cybersecurity", "cyber security", "information security", "infosec"],
    "penetration testing": ["penetration testing", "pen testing", "pentesting"],
    "networking":       ["networking", "computer networks", "tcp ip"],
    "cryptography":     ["cryptography", "encryption"],

    # ── Soft & Other ───────────────────────────────────────────────────────
    "agile":        ["agile", "scrum", "kanban"],
    "rest api":     ["rest", "restful", "rest api"],
    "microservices":["microservices", "microservice"],
    "system design":["system design"],
    "oop":          ["oop", "object oriented", "object-oriented programming"],
    "data structures": ["data structures", "algorithms", "dsa"],
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text


def extract_skills(text):
    text = clean_text(text)
    found_skills = []
    for skill, variations in SKILL_ALIASES.items():
        for var in variations:
            pattern = r'\b' + re.escape(var) + r'\b'
            if re.search(pattern, text):
                found_skills.append(skill)
                break
    return sorted(list(set(found_skills)))