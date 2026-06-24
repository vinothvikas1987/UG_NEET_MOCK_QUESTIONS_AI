import json
import re

def looks_gibberish(text):
    """Detect gibberish or meaningless option text."""
    if not text:
        return True

    text = text.strip()
    if len(text) == 0:
        return True

    # Allow numbers, scientific notations, symbols, units
    if re.fullmatch(r"[\d\.\-×xX*eE\+\–⁻¹⁰⁶⁵⁴⁷⁸⁹⁰%:\sA-Za-z/()^=,+–Δ±∞²³]+", text):
        return False

    # Too many non-alphanumeric chars
    letters = sum(c.isalpha() for c in text)
    non_letters = len(text) - letters
    if letters == 0 and non_letters > 3:
        return True
    if non_letters / len(text) > 0.8:
        return True

    return False


# --- Load JSON ---
with open(r"D:\NEET\llm_extraction\merged_questions_2024.json", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []

for q in data:
    q_num = q.get("question_number", "?")
    question_text = q.get("question_text", "").strip()
    options = q.get("options", {})
    options_diag = q.get("options_diagram_description")

    # --- NEW RULE: Remove questions where question_text is only the number ---
    if re.fullmatch(rf"{re.escape(str(q_num))}\.?", question_text):
        print(f"❌ Skipping Q{q_num}: question_text contains only the question number")
        continue

    # ✅ NEW RULE: If it's a "Match the following" type question, skip option cleaning
    if re.search(r"\bmatch\b", question_text, re.IGNORECASE):
        cleaned.append(q)
        print(f"🤝 Keeping Q{q_num}: 'Match' type question (skipping option validation)")
        continue

    # ✅ CASE 1: No options, but diagram options exist → KEEP
    if (not options or all(not v or not str(v).strip() for v in options.values())) and options_diag:
        cleaned.append(q)
        print(f"🖼️ Keeping Q{q_num}: options empty but diagram options exist")
        continue

    # ✅ CASE 2: Normal option-based question
    if not options or not isinstance(options, dict):
        continue

    # Remove gibberish options
    filtered_options = {k: v for k, v in options.items() if not looks_gibberish(v)}

    # Skip question if fewer than 4 valid options remain and no diagram
    if len(filtered_options) < 4 and not options_diag:
        print(f"⚠️ Skipping Q{q_num}: Not enough valid options and no diagram options")
        continue

    # Replace with filtered options
    q["options"] = filtered_options
    cleaned.append(q)

# --- Save cleaned JSON ---
output_path = r"D:\NEET\llm_extraction\questions_cleaned_for_training_2024.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=4)

print(f"✅ Cleaned data saved to {output_path}")
print(f"Total questions kept: {len(cleaned)}")





# import re
# import json
# import fitz  # PyMuPDF
# import os
# import base64
# from io import BytesIO
# from PIL import Image

# def extract_questions_with_diagrams(pdf_path, output_img_dir="diagrams_1"
# ""):
#     """
#     Extract questions, options, answers, and associated diagrams from a NEET PDF
#     """
#     doc = fitz.open(pdf_path)
#     os.makedirs(output_img_dir, exist_ok=True)
    
#     # Data structures to store extracted content
#     questions = []
#     image_data = []  # Store all extracted images with metadata
#     text_blocks = []  # Store all text blocks with coordinates
    
#     # First pass: Extract all images and text with their positions
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
        
#         # Extract images with their bounding boxes
#         image_list = page.get_images(full=True)
#         for img_index, img in enumerate(image_list):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             if base_image:
#                 image_bytes = base_image["image"]
#                 image_ext = base_image["ext"]
#                 image_bbox = page.get_image_bbox(img)
                
#                 image_data.append({
#                     "page": page_num,
#                     "index": img_index,
#                     "bbox": image_bbox,
#                     "bytes": image_bytes,
#                     "ext": image_ext
#                 })
        
#         # Extract text with bounding boxes
#         text_dict = page.get_text("dict")
#         for block in text_dict["blocks"]:
#             if 'lines' in block:  # It's a text block
#                 bbox = block["bbox"]
#                 full_text = ""
#                 for line in block["lines"]:
#                     for span in line["spans"]:
#                         full_text += span["text"]
                
#                 text_blocks.append({
#                     "page": page_num, 
#                     "bbox": bbox, 
#                     "text": full_text
#                 })
    
#     # Extract all text for regex parsing
#     full_text = ""
#     for page in doc:
#         full_text += page.get_text() + "\n"
    
#     # Find questions using regex
#     question_pattern = re.compile(
#         r"(\d+)\.\s+(.*?)(?=\(\d+\))((?:\(\d+\).*?)+)Answer\s*\(?(\d*)\)?", 
#         re.DOTALL
#     )
#     option_pattern = re.compile(r"\((\d+)\)\s*(.*?)(?=(\(\d+\)|$))", re.DOTALL)
    
#     # Process each question found
#     for match in question_pattern.finditer(full_text):
#         q_number = match.group(1)
#         q_text = match.group(2).strip()
#         options_text = match.group(3)
#         answer = match.group(4).strip()
#         options = []
        
#         # Process options
#         for opt_match in option_pattern.finditer(options_text):
#             opt_number = opt_match.group(1)
#             opt_text = opt_match.group(2).strip()
#             options.append({
#                 "option_number": opt_number,
#                 "option_text": opt_text
#             })
        
#         # Find the text block for this question
#         question_text_blocks = []
#         for tb in text_blocks:
#             if q_number in tb["text"] and q_text[:20] in tb["text"]:
#                 question_text_blocks.append(tb)
        
#         # Find associated diagram for this question
#         diagram_data = None
#         if question_text_blocks:
#             # Use the first matching text block
#             q_block = question_text_blocks[0]
#             diagram_data = find_associated_diagram(q_block, image_data)
        
#         # Save diagram if found
#         diagram_filename = None
#         if diagram_data:
#             diagram_filename = f"q_{q_number}_diagram.{diagram_data['ext']}"
#             diagram_path = os.path.join(output_img_dir, diagram_filename)
#             with open(diagram_path, "wb") as f:
#                 f.write(diagram_data["bytes"])
        
#         questions.append({
#             "question_number": q_number,
#             "question_text": q_text,
#             "options": options,
#             "correct_answer": answer,
#             "diagram_filename": diagram_filename
#         })
    
#     doc.close()
#     return questions

# def find_associated_diagram(question_block, image_data):
#     """
#     Find the diagram most likely associated with a question
#     based on spatial proximity on the same page
#     """
#     q_page = question_block["page"]
#     q_bbox = question_block["bbox"]  # (x0, y0, x1, y1)
    
#     # Filter images on the same page
#     page_images = [img for img in image_data if img["page"] == q_page]
    
#     if not page_images:
#         return None
    
#     # Find the closest image below the question text
#     # We consider images whose top is below the bottom of the question text
#     candidate_images = []
#     for img in page_images:
#         img_bbox = img["bbox"]
#         # Image is below question if its top (y0) is greater than question's bottom (y1)
#         if img_bbox[1] > q_bbox[3]:
#             # Calculate vertical distance
#             distance = img_bbox[1] - q_bbox[3]
#             candidate_images.append((distance, img))
    
#     if not candidate_images:
#         # If no images below, consider any image on the page
#         candidate_images = [(0, img) for img in page_images]
    
#     # Sort by distance and return the closest one
#     candidate_images.sort(key=lambda x: x[0])
#     return candidate_images[0][1] if candidate_images else None

# def save_to_json(questions, output_path):
#     """Save questions to JSON file"""
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(questions, f, ensure_ascii=False, indent=4)

# # Usage
# if __name__ == "__main__":
#     pdf_path = r"D:\NEET\pdf\2025_a-2-46-2.pdf"
#     questions = extract_questions_with_diagrams(pdf_path)
#     save_to_json(questions, "questions_with_diagrams_1.json")
#     print(f"Extracted {len(questions)} questions with diagrams")

