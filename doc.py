# import pdfplumber
# import re
# import json
# import os

# # ==== CONFIG ====
# pdf_path = r"D:\NEET\pdf\2025-1-2-ocr.pdf"   # <-- change if needed
# output_dir = "output"
# os.makedirs(output_dir, exist_ok=True)
# output_file = os.path.join(output_dir, "questions_extracted_.json")

# # ==== REGEX ====
# q_start_re = re.compile(r'^\s*(\d{1,2})\s+(?=[A-Za-z(])')  # question starts with number
# opt_re = re.compile(r'^([1-4])\.\s*(.*)')                  # options start with 1. 2. 3. 4.

# def save_question(serial, q_parts, options):
#     return {
#         "serial_no": str(serial),
#         "question": " ".join(q_parts).strip(),
#         "options": options,
#         "images": []
#     }

# all_questions = []
# expected_serial = 1
# current_q = None
# q_parts = []
# options = []
# collecting_question = False

# with pdfplumber.open(pdf_path) as pdf:
#     for page_num, page in enumerate(pdf.pages, start=1):
#         text = page.extract_text() or ""
#         lines = text.splitlines()

#         for line in lines:
#             line = line.strip()
#             if not line:
#                 continue

#             # --- Detect new question ---
#             m_q = q_start_re.match(line)
#             if m_q:
#                 q_num = int(m_q.group(1))

#                 # Save previous if valid
#                 if current_q and options:
#                     all_questions.append(save_question(current_q, q_parts, options))

#                 # Reset for new Q
#                 current_q = q_num
#                 expected_serial = q_num + 1
#                 q_parts = []
#                 options = []
#                 collecting_question = True

#                 # Remove Q number and keep rest
#                 rest = line[m_q.end():].strip()
#                 if rest.startswith("1."):   # means options started on same line
#                     collecting_question = False
#                     options.append(rest)
#                 else:
#                     if "1." in rest:  # inline first option
#                         before_opt, opt_part = rest.split("1.", 1)
#                         q_parts.append(before_opt.strip())
#                         options.append("1. " + opt_part.strip())
#                         collecting_question = False
#                     else:
#                         q_parts.append(rest)
#                 continue

#             # --- Still collecting question ---
#             if collecting_question:
#                 if line.startswith("1."):
#                     collecting_question = False
#                     options.append(line)
#                 else:
#                     q_parts.append(line)
#                 continue

#             # --- Collect options ---
#             if not collecting_question and current_q:
#                 m_opt = opt_re.match(line)
#                 if m_opt:
#                     options.append(line)
#                     if line.startswith("4."):  # last option → save
#                         all_questions.append(save_question(current_q, q_parts, options))
#                         current_q = None
#                         q_parts = []
#                         options = []
#                 else:
#                     # continuation of previous option
#                     if options:
#                         options[-1] += " " + line

# # Write JSON output
# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(all_questions, f, ensure_ascii=False, indent=2)

# print(f"✅ Extracted {len(all_questions)} questions")
# print(f"Saved to {output_file}")

import pdfplumber
import re
import json
import os

pdf_path = r"D:\\NEET\\pdf\\2025-1-2-ocr.pdf"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Regex patterns
# q_start_re = re.compile(r"^(\d{1,3})\s+(?=[A-Za-z(])")
# q_start_re = re.compile(r"^(\d{1,3})(?=\s+[A-Z(])")  # capital letter or '(' after space
q_start_re = re.compile(r'^\s*(\d{1,2})\s+(?=[A-Z(])')

opt_re = re.compile(r"^([1-4]\.\s*.+)")

all_questions = []
global expected_serial
expected_serial = 1  # Start from Q1

def save_question(serial, q_parts, options):
    return {
        "serial_no": str(serial),
        "question": " ".join(q_parts).strip(),
        "options": options,
        "images": []
    }
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        width, height = page.width, page.height

        # Left and right columns
        left_text = page.within_bbox((0, 0, width/2, height)).extract_text() or ""
        right_text = page.within_bbox((width/2, 0, width, height)).extract_text() or ""

        print(f"\n=== Page {page_num} - LEFT COLUMN ===")
        print(left_text.strip() if left_text.strip() else "[No text extracted]")

        print(f"\n=== Page {page_num} - RIGHT COLUMN ===")
        print(right_text.strip() if right_text.strip() else "[No text extracted]")


        for col_text in [left_text, right_text]:
            if not col_text.strip():
                continue

            lines = col_text.strip().splitlines()
            current_q = None
            q_parts = []
            options = []
            collecting_question = False

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Detect question start
                m_q = q_start_re.match(line)
                if m_q:
                    q_num = int(m_q.group(1))

                    # Check for missing questions
                   
                    if q_num != expected_serial:
                        print(f"⚠ Missing Q{expected_serial}, found Q{q_num}")
                        expected_serial = q_num

                    # Save previous if complete
                    if current_q and options:
                        all_questions.append(save_question(current_q, q_parts, options))

                    current_q = q_num
                    expected_serial = current_q + 1
                    q_parts = []
                    options = []
                    collecting_question = True

                    rest = line[m_q.end():].strip()
                    if rest.startswith("1."):
                        collecting_question = False
                        options.append(rest)
                    else:
                        if "1." in rest:
                            before_opt, opt_part = rest.split("1.", 1)
                            q_parts.append(before_opt.strip())
                            options.append("1. " + opt_part.strip())
                            collecting_question = False
                        else:
                            q_parts.append(rest)
                    continue

                # If collecting question text
                if collecting_question:
                    if line.startswith("1."):
                        collecting_question = False
                        options.append(line)
                    else:
                        q_parts.append(line)
                    continue

                # Collecting options
                if not collecting_question and current_q:
                    if opt_re.match(line):
                        options.append(line)
                        if line.startswith("4."):
                            all_questions.append(save_question(current_q, q_parts, options))
                            current_q = None
                            q_parts = []
                            options = []
                    else:
                        if options:
                            options[-1] += " " + line

# Save to file
with open(os.path.join(output_dir, "questions_with_options.json"), "w", encoding="utf-8") as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(all_questions)} questions")


# from pdf2docx import Converter

# # Input and output paths
# pdf_file = r"D:\NEET\pdf\2025-1-2-ocr.pdf"
# docx_file = r"D:\NEET\pdf\2025-1-2.docx"

# # Create converter
# cv = Converter(pdf_file)

# # Convert all pages (or specify a range: start=0, end=5)
# cv.convert(docx_file, start=0, end=None)

# # Close converter
# cv.close()

# print(f"✅ PDF successfully converted to Word: {docx_file}")

