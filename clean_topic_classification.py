import json
import re

# === define subject breakpoints ===
subject_breaks = [
    (50, "Physics"),
    (98, "Chemistry"),
    (198, "Biology"),
    (242, "Physics"),
    (288, "Chemistry"),
    (379, "Biology"),
    (428, "Physics"),
    (477, "Chemistry"),
    (577, "Biology"),
    (622, "Physics"),
    (666, "Chemistry"),
    (756, "Biology"),
]

def get_subject(qnum):
    for end, subject in subject_breaks:
        if qnum <= end:
            return subject
    return "Unknown"

# === load JSON ===
with open(r"D:\NEET\classified_questions.json",  encoding="utf-8") as f:
    data = json.load(f)

# === process each question ===
for q in data:
    qnum = int(q["question_number"])
    
    # assign subject based on number
    q["Subject"] = get_subject(qnum)
    
    # clean up leading numbering in question_text (for 199–379)
    if 199 <= qnum <= 379:
        q["question_text"] = re.sub(r"^\s*\d+\.\s*", "", q["question_text"])

# === save updated JSON ===
with open("cleaned_classified_questions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Updated subjects and cleaned text saved to updated_questions.json")




















