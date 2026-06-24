# import json
# import os

# # Folder containing your JSON files
# folder_path = r"D:\NEET\llm_extraction\cleaned"  # Change this to your directory path if needed
# output_file = "cleaned_merged_questions.json"

# # Get all JSON files in the folder
# json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

# merged_data = []
# question_counter = 1

# for filename in json_files:
#     filepath = os.path.join(folder_path, filename)
#     with open(filepath, "r", encoding="utf-8") as f:
#         try:
#             data = json.load(f)
#         except json.JSONDecodeError:
#             print(f"❌ Skipping invalid JSON: {filename}")
#             continue

#         for q in data:
#             q["question_number"] = str(question_counter)
#             merged_data.append(q)
#             question_counter += 1

# # Save merged JSON
# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(merged_data, f, indent=2, ensure_ascii=False)

# print(f"✅ Merged {len(json_files)} files into '{output_file}' with {len(merged_data)} questions total.")


import json

input_file = r"D:\NEET\llm_extraction\cleaned\merged_questions_cleaned.json"   # your input file
output_file = "renumbered_questions.json"  # output file name

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Reassign question numbers continuously
for i, q in enumerate(data, start=1):
    q["question_number"] = str(i)

# Save updated JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✅ Renumbered {len(data)} questions in '{output_file}' from 1 to {len(data)}.")
