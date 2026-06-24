import json

# 1. Load your original JSON data
input_file_path = r"D:\NEET\classified_questions.json"  # Using raw string for Windows path
output_file_path = r"D:\NEET\training_data.jsonl"

try:
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        original_data = json.load(infile)  # This should be your list of questions

    # 2. Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        # 3. Loop through each question in the original data
        for item in original_data:
            # Build the options list in the required format
            options_list = []
            for opt in item['options']:
                # Create a new dictionary for each option, excluding 'image_option'
                option_dict = {
                    "option_number": opt['option_number'],
                    "option_text": opt['option_text'].replace('\n', ' ')  # Clean up newlines
                }
                options_list.append(option_dict)
            
            # Create the structured text for the model
            training_example = {
                "question": item['question'].replace('\n', ' '),
                "options": options_list,
                "answer": item['answer'],
                "Subject": item['Subject'],
                "Topic": item['Topic'],
                "Subtopic": item['Subtopic']
            }
            
            # Convert the structured data to a JSON string
            training_json_str = json.dumps(training_example, ensure_ascii=False)
            
            # Create the final text prompt in the required instruction-response format
            final_text = f"### Instruction: Generate a multiple choice physics question with four options, an answer key, and topic metadata. ### Response: {training_json_str}"
            
            # Write the final text as one line in the JSONL file
            outfile.write(json.dumps({"text": final_text}, ensure_ascii=False) + '\n')
    
    print(f"Success! Converted {len(original_data)} questions.")
    print(f"Output saved to: {output_file_path}")

except FileNotFoundError:
    print(f"Error: The file {input_file_path} was not found. Please check the path.")
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in the input file: {e}")
except KeyError as e:
    print(f"Error: Missing expected key in JSON data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")