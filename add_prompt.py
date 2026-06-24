import json
import re
import ast

def clean_diagram_descriptions(desc):
    """
    Cleans diagram description strings by removing image filenames like
    'page1_diagram_3.jpeg -' or similar patterns before the actual text.
    """
    if not desc or str(desc).lower() in ["none", "null", ""]:
        return desc

    try:
        # Parse if it's a stringified dict
        desc_dict = ast.literal_eval(desc) if isinstance(desc, str) else desc
        if isinstance(desc_dict, dict):
            cleaned = {}
            for key, value in desc_dict.items():
                if isinstance(value, str):
                    # Remove leading image filenames and dash/spaces
                    value = re.sub(r"^\s*[\w\-]+\.jpe?g\s*-\s*", "", value.strip())
                    cleaned[key] = value
                else:
                    cleaned[key] = value
            return cleaned
    except Exception:
        pass

    # If it's just a string, clean directly
    if isinstance(desc, str):
        return re.sub(r"^\s*[\w\-]+\.jpe?g\s*-\s*", "", desc.strip())
    return desc


# Load your question dataset
with open(r"D:\NEET\cleaned_classified_questions.json", encoding="utf-8") as f:
    data = json.load(f)

dataset = []

for q in data:
    # Remove Subtopic field
    q.pop("Subtopic", None)

    # Clean diagram descriptions (remove .jpeg prefixes)
    q["question_diagram_description"] = clean_diagram_descriptions(q.get("question_diagram_description", ""))
    q["options_diagram_description"] = clean_diagram_descriptions(q.get("options_diagram_description", ""))

    subject = q.get("Subject", "Unknown")
    topic = q.get("Topic", "Unknown")

    q_diag = str(q.get("question_diagram_description", "")).strip().lower()
    o_diag = str(q.get("options_diagram_description", "")).strip().lower()

    # Check if either question or options contain valid diagram description
    has_diagram = q_diag not in ["none", "null", ""] or o_diag not in ["none", "null", ""]

    prompt_type = "with a diagram" if has_diagram else "without a diagram"
    prompt = f"Generate a {subject} question on the topic '{topic}' {prompt_type}."

    # Create response JSON string
    response = json.dumps(q, ensure_ascii=False)

    dataset.append({"prompt": prompt, "completion": response})

# Save dataset as JSONL
with open("added_prompt.jsonl", "w", encoding="utf-8") as f:
    for item in dataset:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("✅ train_data.jsonl created successfully (cleaned diagram names, removed Subtopic).")
