import os
import re
import json
import torch
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_ID = os.environ.get("MODELID")
CONTACT_EMAIL = "vinothvikas1987@gmail.com"
MAX_FREE = 5
API_KEY = os.environ.get("APIKEY")

usage_db = {}

SUBJECTS_TOPICS = {
    "Physics": [
        "Physics and Measurement", "Kinematics", "Laws of Motion",
        "Work, Energy, and Power", "Rotational Motion", "Gravitation",
        "Properties of Solids and Liquids", "Thermodynamics",
        "Kinetic Theory of Gases", "Oscillations and Waves",
        "Electrostatics", "Current Electricity",
        "Magnetic Effects of Current and Magnetism",
        "Electromagnetic Induction and Alternating Currents",
        "Electromagnetic Waves", "Optics",
        "Dual Nature of Matter and Radiation", "Atoms and Nuclei",
        "Electronic Devices", "Experimental Skills"
    ],
    "Chemistry": [
        "Some Basic Concepts of Chemistry", "Structure of Atom",
        "Classification of Elements and Periodicity in Properties",
        "Chemical Bonding and Molecular Structure",
        "States of Matter: Gases and Liquids", "Thermodynamics",
        "Equilibrium", "Redox Reactions", "Hydrogen",
        "s-Block Elements", "p-Block Elements",
        "Organic Chemistry: Basic Principles and Techniques",
        "Hydrocarbons", "Environmental Chemistry", "Solid State",
        "Solutions", "Electrochemistry", "Chemical Kinetics",
        "Surface Chemistry", "Isolation of Elements"
    ],
    "Botany": [
        "Diversity in the Living World",
        "Structural Organisation in Plants and Animals",
        "Cell Structure and Function", "Plant Physiology",
        "Human Physiology", "Reproduction",
        "Genetics and Evolution", "Biology and Human Welfare",
        "Biotechnology", "Ecology and Environment"
    ],
    "Zoology": [
        "Animal Kingdom", "Structural Organisation in Animals",
        "Animal Physiology", "Human Physiology", "Reproduction",
        "Genetics and Evolution", "Biology and Human Welfare",
        "Biotechnology", "Ecology and Environment"
    ]
}

print("Loading model...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
print("Model loaded!")

def generate(subject, topic):
    prompt = f"Generate a {subject} question on the topic '{topic}' without a diagram."
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=300, temperature=0.7)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    json_blocks = re.findall(r'\{.*?\}(?=\{|\Z)', result, re.DOTALL)
    for block in json_blocks:
        try:
            d = json.loads(block)
            lines = [
                f"**Subject:** {d.get('Subject', 'N/A')}",
                f"**Topic:** {d.get('Topic', 'N/A')}",
                "",
                f"**Q{d.get('question_number', '?')}.** {d.get('question_text', '').strip()}",
                "",
                "**Options:**"
            ]
            for i, opt in enumerate(d.get('options', {}).values(), 1):
                lines.append(f"  {i}. {opt}")
            lines.append(f"\n**Correct Answer:** Option {d.get('answer', 'N/A')}")
            return "\n".join(lines)
        except json.JSONDecodeError:
            continue
    return "Could not generate a valid question. Try again."

def check_key(key):
    if key == API_KEY:
        return gr.update(visible=False), gr.update(visible=True), ""
    return gr.update(visible=True), gr.update(visible=False), "Invalid key. Try again."

def update_topics(subject):
    return gr.Dropdown(choices=SUBJECTS_TOPICS[subject], value=SUBJECTS_TOPICS[subject][0])

def on_generate(subject, topic, email, count):
    if not email or "@" not in email:
        return "Please enter a valid email address.", count, gr.update(interactive=True)

    if email not in usage_db:
        usage_db[email] = 0

    if usage_db[email] >= MAX_FREE:
        return (
            f"**Free limit reached!**\n\n"
            f"You have used all 5 free questions.\n\n"
            f"Contact **{CONTACT_EMAIL}** for unlimited access."
        ), count, gr.update(interactive=False)

    result = generate(subject, topic)
    usage_db[email] += 1
    count = usage_db[email]

    if count >= MAX_FREE:
        result += (
            f"\n\n---\n**Free limit reached!** "
            f"Email **{CONTACT_EMAIL}** for unlimited access."
        )
        return result, count, gr.update(interactive=False)

    remaining = MAX_FREE - count
    result += f"\n\n*{remaining} free question(s) remaining for {email}*"
    return result, count, gr.update(interactive=True)

with gr.Blocks(title="NEET Question Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# NEET Question Generator")

    with gr.Group(visible=True) as key_screen:
        gr.Markdown("### Enter your access key to continue")
        key_input = gr.Textbox(label="Access Key", type="password")
        key_error = gr.Markdown("")
        key_btn = gr.Button("Submit", variant="primary")

    with gr.Group(visible=False) as main_screen:
        gr.Markdown("### Select subject and topic to generate NEET-style MCQs")
        email_input = gr.Textbox(label="Your Email", placeholder="you@example.com")
        state = gr.State(0)

        with gr.Row():
            subject_dd = gr.Dropdown(choices=list(SUBJECTS_TOPICS.keys()), label="Subject", value="Physics")
            topic_dd = gr.Dropdown(choices=SUBJECTS_TOPICS["Physics"], label="Topic")

        subject_dd.change(fn=update_topics, inputs=subject_dd, outputs=topic_dd)

        btn = gr.Button("Generate Question", variant="primary")
        output = gr.Markdown()

        btn.click(
            fn=on_generate,
            inputs=[subject_dd, topic_dd, email_input, state],
            outputs=[output, state, btn]
        )

    key_btn.click(
        fn=check_key,
        inputs=[key_input],
        outputs=[key_screen, main_screen, key_error]
    )

if __name__ == "__main__":
    demo.launch()
