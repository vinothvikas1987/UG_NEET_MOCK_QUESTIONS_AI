import json

# Input and output files
input_file = r"D:\NEET\questions_with_diagrams_1.json"
output_file = r"D:\NEET\questions_with_diagrams_train.jsonl"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(output_file, "w", encoding="utf-8") as out_f:
    for item in data:
        # Build options as text
        options_text = "\n".join(
            [f"({opt['option_number']}) {opt['option_text']}" for opt in item["options"]]
        )

        # Question + options text
        q_text = f"{item['question_text']}\nOptions:\n{options_text}"

        # Final answer text
        correct_option = next(
            (opt["option_text"] for opt in item["options"] if opt["option_number"] == item["correct_answer"]),
            None
        )
        answer_text = f"Answer: ({item['correct_answer']}) {correct_option}"

        # Build training entry
        train_entry = {
            "instruction": "Generate a NEET-style MCQ with 4 options and the correct answer, given a diagram.",
            "input": {
                "image": f"diagrams_1/{item['diagram_filename']}",
                "text": q_text
            },
            "output": f"{q_text}\n{answer_text}"
        }

        out_f.write(json.dumps(train_entry, ensure_ascii=False) + "\n")

print(f"✅ Reformatted dataset saved as {output_file}")
