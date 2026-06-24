import json

# --- File paths ---
base_file = r"D:\NEET\llm_extraction\no_diagram_questions_2024.json"
extra_file = r"D:\NEET\llm_extraction\questions_with_dia_explanation_2024.json"
output_file = r"D:\NEET\llm_extraction\merged_questions_2024.json"

# --- Load both JSON files ---
with open(base_file, "r", encoding="utf-8") as f:
    base_questions = json.load(f)

with open(extra_file, "r", encoding="utf-8") as f:
    extra_questions = json.load(f)

# --- Convert base to dict for quick lookup by question number ---
base_dict = {q["question_number"]: q for q in base_questions}

# --- Filter and merge ---
for q in extra_questions:
    qnum = q.get("question_number")
    q_diag = str(q.get("question_diagram_description", "")).strip()
    opt_diag = str(q.get("options_diagram_description", "")).strip()

    # Skip if "Aakash" is present in any diagram text
    if "aakash" in q_diag.lower() or "aakash" in opt_diag.lower():
        continue

    # Merge only if that question number exists in base
    if qnum in base_dict:
        if q_diag and q_diag.lower() != "null":
            base_dict[qnum]["question_diagram_description"] = q_diag
        if opt_diag and opt_diag.lower() != "null":
            base_dict[qnum]["options_diagram_description"] = opt_diag

# --- Convert back to list (maintain original ordering) ---
merged_list = [base_dict[q["question_number"]] for q in base_questions]

# --- Save merged result ---
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_list, f, indent=4, ensure_ascii=False)

print(f"✅ Merged file created: {output_file}")
