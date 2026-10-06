import json
import os
from pathlib import Path

repo_dir = Path(r"C:\Users\Akshay Kumar\code\master-resume-engineer")
assets_dir = repo_dir / "assets"
docs_dir = repo_dir / "docs"
docs_dir.mkdir(exist_ok=True)

resumes = {
    "master": {
        "title": "Master Executive Resume (SSOT)",
        "role": "Analytics Engineer & STEM MBA",
        "file": "Akshay_Kumar_Master_Resume.md",
        "description": "Comprehensive single-source-of-truth master document encompassing 7+ years of data engineering, federal decision support, and banking risk pipelines."
    },
    "analytics_engineer": {
        "title": "Data & Analytics Engineer",
        "role": "ETL, Distributed Pipelines & Data Modeling",
        "file": "Akshay_Kumar_Resume_Data_Analytics_Engineer.md",
        "description": "Hardened for senior Data Engineering & Analytics roles emphasizing Python, SQL, DuckDB, RESTful pipelines, and 97M+ record banking verification."
    },
    "operations_manager": {
        "title": "Operations & Analytics Manager",
        "role": "Capacity Modeling & Process Transformation",
        "file": "Akshay_Kumar_Resume_Operations_Analytics_Manager.md",
        "description": "Tailored for operational leadership and business intelligence roles highlighting consular throughput scaling (+30%) and triage automation (-65%)."
    },
    "product_manager": {
        "title": "Technical Product Manager",
        "role": "Enterprise AI, Analytics & Systems Strategy",
        "file": "Akshay_Kumar_Resume_Technical_Product_Manager.md",
        "description": "Structured for TPM opportunities uniting user-centric product discovery, consular diagnostic platforms, and high-throughput data architectures."
    }
}

resume_data = {}
for key, meta in resumes.items():
    file_path = assets_dir / meta["file"]
    if file_path.is_file():
        text = file_path.read_text(encoding="utf-8")
        resume_data[key] = {
            "title": meta["title"],
            "role": meta["role"],
            "description": meta["description"],
            "content": text
        }

with open(docs_dir / "resumes_data.json", "w", encoding="utf-8") as f:
    json.dump(resume_data, f, indent=2)

print(f"Loaded {len(resume_data)} resumes into docs/resumes_data.json")
