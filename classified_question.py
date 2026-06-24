import json
import subprocess

# ---------- Load syllabus ----------
print("[DEBUG] Loading syllabus.json...")
with open("syllabus.json", "r", encoding="utf-8") as f:
    syllabus = json.load(f)
print(f"[DEBUG] Loaded syllabus with {len(syllabus)} subjects.")

# Flatten syllabus for easy searching
syllabus_entries = []
for subject in syllabus:
    for unit in subject["Units"]:
        syllabus_entries.append({
            "Subject": subject["Subject"],
            "Topic": unit["Topic"],
            "Subtopic": unit["Subtopic"]
        })
print(f"[DEBUG] Created flattened syllabus with {len(syllabus_entries)} entries.")


def run_ollama(prompt):
    """Helper to call Ollama and return the model output."""
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        capture_output=True,
    )
    return result.stdout.decode("utf-8", errors="ignore")


def classify_question_text(question_text, diagram_text, options_diagram_text, syllabus_entries):
    # Combine all possible content
    combined_text = f"{question_text}\n\nDiagram Description: {diagram_text}\n\nOptions Diagram Description: {options_diagram_text}"

    # Prepare candidate topics and subtopics
    topics = sorted(list({entry["Topic"] for entry in syllabus_entries}))
    subtopics = []
    for entry in syllabus_entries:
        subtopics.extend(entry["Subtopic"].split(","))
    subtopics = sorted(list(set([s.strip() for s in subtopics if s.strip()])))

    # Step 1: Predict Topic
    prompt_topic = f"""
You are a NEET syllabus classifier.
Given a question, identify the most appropriate **Topic** from the following list.

Return only JSON like:
{{"Topic": "..."}} 

Available Topics:
{json.dumps(topics, indent=2)}

Question content:
{combined_text}
"""
    print("[DEBUG] Calling Ollama for Topic classification...")
    response_topic = run_ollama(prompt_topic)

    try:
        topic_json = json.loads(response_topic)
        topic = topic_json.get("Topic", "Unknown")
    except json.JSONDecodeError:
        topic = "Unknown"
    print(f"[DEBUG] Predicted Topic: {topic}")

    # Step 2: Predict Subtopic
    prompt_subtopic = f"""
You are a NEET syllabus classifier.
Given the question and predicted Topic = '{topic}', identify the most suitable **Subtopic**.

Return only JSON like:
{{"Subtopic": "..."}} 

Available Subtopics:
{json.dumps(subtopics, indent=2)}

Question content:
{combined_text}
"""
    print("[DEBUG] Calling Ollama for Subtopic classification...")
    response_subtopic = run_ollama(prompt_subtopic)

    try:
        subtopic_json = json.loads(response_subtopic)
        subtopic = subtopic_json.get("Subtopic", "Unknown")
    except json.JSONDecodeError:
        subtopic = "Unknown"

    print(f"[DEBUG] Predicted Subtopic: {subtopic}")

    # Subject = the one that matches this topic in the syllabus
    subject = "Unknown"
    for entry in syllabus_entries:
        if entry["Topic"] == topic:
            subject = entry["Subject"]
            break

    return subject, topic, subtopic


# ---------- Load questions ----------
print("[DEBUG] Loading questions.json...")
with open(r"D:\NEET\llm_extraction\cleaned\renumbered_questions.json", encoding="utf-8") as f:
    questions = json.load(f)
print(f"[DEBUG] Loaded {len(questions)} questions.")


classified_questions = []

for q in questions:
    print(f"\n[DEBUG] --- Classifying Question {q['question_number']} ---")

    question_text = q.get("question_text", "")
    diagram_text = q.get("question_diagram_description", "")
    options_diagram_text = q.get("options_diagram_description", "")

    subject, topic, subtopic = classify_question_text(
        question_text, diagram_text, options_diagram_text, syllabus_entries
    )

    q["Subject"] = subject
    q["Topic"] = topic
    q["Subtopic"] = subtopic

    print(f"[DEBUG] Classified as Subject: {subject}, Topic: {topic}, Subtopic: {subtopic}")
    classified_questions.append(q)


print("\n[DEBUG] Saving classified questions to classified_questions.json...")
with open("classified_questions.json", "w", encoding="utf-8") as f:
    json.dump(classified_questions, f, indent=2, ensure_ascii=False)

print("✅ Classification completed using question text and diagram descriptions.")



# import json
# import subprocess
# import re
# from difflib import get_close_matches


# print("[DEBUG] Loading syllabus.json...")
# with open("syllabus.json", "r", encoding="utf-8") as f:
#     syllabus = json.load(f)
# print(f"[DEBUG] Loaded syllabus with {len(syllabus)} subjects.")


# # Flatten syllabus for quick searching
# syllabus_entries = []
# for subject in syllabus:
#     subject_name = subject["Subject"]
#     for unit in subject["Units"]:
#         syllabus_entries.append({
#             "Subject": subject_name,
#             "Topic": unit["Topic"],
#             "Subtopic": unit["Subtopic"]
#         })
# print(f"[DEBUG] Created flattened syllabus with {len(syllabus_entries)} entries.")


# def get_subject_syllabus(question_number, syllabus):
#     qn = int(question_number)
#     if 1 <= qn <= 45:
#         print("[DEBUG] Filtering syllabus for Physics")
#         return [entry for entry in syllabus if entry["Subject"] == "Physics"]
#     elif 46 <= qn <= 90:
#         print("[DEBUG] Filtering syllabus for Chemistry")
#         return [entry for entry in syllabus if entry["Subject"] == "Chemistry"]
#     elif 91 <= qn <= 180:
#         print("[DEBUG] Filtering syllabus for Botany and Zoology")
#         return [entry for entry in syllabus if entry["Subject"] in ["Botany", "Zoology"]]
#     else:
#         print("[DEBUG] Question number out of expected range, using full syllabus")
#         return syllabus


# def split_subtopics(subtopic_string):
#     # Split on commas, periods, semicolons that are NOT inside parentheses
#     # Using regex with negative lookahead/lookbehind for parentheses
#     # We'll replace newlines by space first for safety
#     text = subtopic_string.replace('\n', ' ')

#     # This regex aims to split on ',', '.', ';' not inside parentheses
#     pattern = r'''
#         (          # Capture group for splitting delimiters
#           (?<!\()  # No '(' before
#           [.,;]    # The delimiter
#           (?![^\(\)]*\))  # Not followed by a closing ')' that matches an opening '(' before delimiter
#         )
#     '''
#     # Instead of complicated regex, a safer approach is manual parsing:

#     splits = []
#     current = []
#     depth = 0  # Track parentheses depth
#     for char in text:
#         if char == '(':
#             depth += 1
#         elif char == ')':
#             if depth > 0:
#                 depth -= 1
#         if char in [',', '.', ';'] and depth == 0:
#             # delimiter outside parentheses - split here
#             piece = ''.join(current).strip()
#             if piece:
#                 splits.append(piece)
#             current = []
#         else:
#             current.append(char)
#     # add last piece
#     piece = ''.join(current).strip()
#     if piece:
#         splits.append(piece)
#     return splits


# def classify_with_ollama(question, candidate_entries, classification_type):
#     """classification_type should be 'Topic' or 'Subtopic'"""
#     if classification_type == "Topic":
#         items = sorted(list({entry["Topic"] for entry in candidate_entries}))
#     elif classification_type == "Subtopic":
#         # For subtopics, split each long subtopic string into smaller subtopic pieces
#         items = []
#         for entry in candidate_entries:
#             pieces = split_subtopics(entry["Subtopic"])
#             items.extend(pieces)
#         # Remove duplicates and sort
#         items = sorted(list(set(items)))
#     else:
#         raise ValueError(f"Unknown classification_type: {classification_type}")

#     prompt = f"""
# You are a question classifier.
# Classify the following question into one of the {classification_type.lower()}s listed below.
# Return only JSON in the format:
# {{"{classification_type}": "..."}}

# {classification_type}s:
# {json.dumps(items, indent=2)}

# Question:
# {question}
# """
#     print(f"[DEBUG] Calling Ollama to classify {classification_type}...")
#     result = subprocess.run(
#         ["ollama", "run", "llama3"],
#         input=prompt.encode("utf-8"),
#         capture_output=True,
#     )
#     print(f"[DEBUG] Ollama {classification_type} classification completed.")
#     return result.stdout.decode("utf-8")


# def classify_question(question, question_number, syllabus_entries):
#     print(f"[DEBUG] Classifying question number {question_number} ...")
#     subject_entries = get_subject_syllabus(question_number, syllabus_entries)

#     # Step 1: Classify Topic
#     response_topic = classify_with_ollama(question, subject_entries, "Topic")
#     try:
#         topic_classification = json.loads(response_topic)
#         topic = topic_classification.get("Topic")
#         print(f"[DEBUG] Predicted Topic: {topic}")
#     except json.JSONDecodeError:
#         print("[DEBUG] JSON decode error on Ollama Topic response.")
#         topic = None

#     if not topic:
#         return {"Subject": "Unknown", "Topic": "Unknown", "Subtopic": "Unknown"}

#     # Filter to subtopics under this topic
#     subtopic_candidates = [e for e in subject_entries if e["Topic"] == topic]

#     # Step 2: Classify Subtopic
#     response_subtopic = classify_with_ollama(question, subtopic_candidates, "Subtopic")
#     try:
#         subtopic_classification = json.loads(response_subtopic)
#         subtopic = subtopic_classification.get("Subtopic")
#         print(f"[DEBUG] Predicted Subtopic: {subtopic}")
#     except json.JSONDecodeError:
#         print("[DEBUG] JSON decode error on Ollama Subtopic response.")
#         subtopic = "Unknown"

#     # Subject is consistent from filtered syllabus entries
#     subject = subtopic_candidates[0]["Subject"] if subtopic_candidates else "Unknown"

#     return {
#         "Subject": subject,
#         "Topic": topic,
#         "Subtopic": subtopic
#     }


# print("[DEBUG] Loading questions.json...")
# with open("questions.json", "r", encoding="utf-8") as f:
#     questions = json.load(f)
# print(f"[DEBUG] Loaded {len(questions)} questions.")


# selected_questions = [q for q in questions if int(q["question_number"]) <= 180]
# print(f"[DEBUG] Filtering questions: selected {len(selected_questions)} questions with question_number <= 2.")


# classified_questions = []

# for q in selected_questions:
#     print(f"[DEBUG] --- Classifying Question {q['question_number']} ---")
#     result = classify_question(q["question"], q["question_number"], syllabus_entries)
#     q["Subject"] = result.get("Subject")
#     q["Topic"] = result.get("Topic")
#     q["Subtopic"] = result.get("Subtopic")
#     print(f"[DEBUG] Classified Question {q['question_number']} as Subject: {q['Subject']}, Topic: {q['Topic']}, Subtopic: {q['Subtopic']}")
#     classified_questions.append(q)


# print("[DEBUG] Saving classified questions to classified_questions.json...")
# with open("classified_questions.json", "w", encoding="utf-8") as f:
#     json.dump(classified_questions, f, indent=2, ensure_ascii=False)


# print("✅ Classification completed for selected questions. Saved to classified_questions.json")

