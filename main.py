from flask import Flask, render_template, request, jsonify, send_file
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from fpdf import FPDF
import os

app = Flask(__name__)
 
model = OllamaLLM(model="mistral")

story_data = {"story_so_far": "", "theme": "", "genre": "", "setting": "", "feedback_score": 0}

def generate_story(theme, genre, setting, story_so_far="", user_input=None, end_story=False, feedback_score=0):
    story_so_far_text = f"Story so far: {story_so_far}" if story_so_far else "Start the story from scratch."
    user_input_text = f"User input: {user_input}" if user_input else ""
    
    feedback_adjustment = "Make the story more engaging and unpredictable." if feedback_score > 0 else "Keep it simple and clear."
    
    prompt_text = f"""
    Write a coherent and engaging short story passage (about 100 words) based on these details:
    
    Theme: {theme}
    Genre: {genre}
    Setting: {setting}
    {story_so_far_text}
    {user_input_text}
    
    {feedback_adjustment}
    {"Conclude the story with a satisfying ending." if end_story else "Continue the story smoothly."}
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    formatted_prompt = prompt.format(
        theme=theme, genre=genre, setting=setting,
        story_so_far_text=story_so_far_text, user_input_text=user_input_text
    )
    
    try:
        response = model.invoke(formatted_prompt).strip()
    except Exception as e:
        response = f"Error generating story: {str(e)}"
    
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_story", methods=["POST"])
def start_story():
    data = request.json
    story_data.update({
        "theme": data["theme"],
        "genre": data["genre"],
        "setting": data["setting"],
        "story_so_far": "",
        "feedback_score": 0
    })
    
    story_data["story_so_far"] = generate_story(story_data["theme"], story_data["genre"], story_data["setting"])
    
    return jsonify({"story": story_data["story_so_far"]})

@app.route("/continue_story", methods=["POST"])
def continue_story():
    data = request.json
    user_input = data["user_input"]
    
    story_part = generate_story(
        story_data["theme"], story_data["genre"], story_data["setting"],
        story_data["story_so_far"], user_input, feedback_score=story_data["feedback_score"]
    )
    
    story_data["story_so_far"] += "\n\n" + story_part
    
    return jsonify({"story": story_part, "ended": False})

@app.route("/end_story", methods=["POST"])
def end_story():
    story_ending = generate_story(
        story_data["theme"], story_data["genre"], story_data["setting"],
        story_data["story_so_far"], end_story=True, feedback_score=story_data["feedback_score"]
    )
    
    story_data["story_so_far"] += "\n\n" + story_ending
    
    return jsonify({"story": story_ending, "ended": True})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    feedback = data.get("feedback")
    
    if feedback == "like":
        story_data["feedback_score"] += 1
    elif feedback == "dislike":
        story_data["feedback_score"] -= 1
    
    return jsonify({"message": "Feedback received", "feedback_score": story_data["feedback_score"]})

@app.route("/download_story", methods=["GET"])
def download_story():
    if not story_data["story_so_far"]:
        return jsonify({"error": "No story available to download"}), 400

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Generated Story", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    for paragraph in story_data["story_so_far"].split("\n\n"):
        pdf.multi_cell(0, 10, paragraph)
        pdf.ln(5)

    pdf_filename = "generated_story.pdf"
    pdf.output(pdf_filename)

    return send_file(pdf_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)