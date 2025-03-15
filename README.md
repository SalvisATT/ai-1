# 📖 Flask Story Generator

This is a **Flask-based web application** that generates interactive stories using the **Ollama LLM (Mistral model)**. Users can start a story, continue it with their input, provide feedback, and download the final story as a **PDF**.

---

## 🚀 Features
✔️ Start a new story based on a chosen **theme, genre, and setting**.
✔️ Continue the story interactively with user input.
✔️ Adjust story engagement using **feedback scoring**.
✔️ Download the complete story as a **PDF**.
✔️ Powered by **Flask** and **Langchain Ollama** for AI-driven storytelling.

---

## 🛠️ Setup & Installation

### 🔹 1. Clone the Repository
```sh
git clone https://github.com/yourusername/flask-story-generator.git
cd flask-story-generator
```

### 🔹 2. Create and Activate a Virtual Environment

#### Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 🔹 3. Install Dependencies
```sh
pip install flask langchain_ollama fpdf
```

---

## ▶️ Running the Application
```sh
python app.py
```
Once running, open your browser and go to:
```
http://127.0.0.1:5000/
```

---

## 🌍 API Endpoints

### 📌 `POST /start_story`
**Request Body:**
```json
{
  "theme": "Fantasy",
  "genre": "Adventure",
  "setting": "Medieval castle"
}
```
**Response:**
```json
{
  "story": "Once upon a time..."
}
```

### 📌 `POST /continue_story`
**Request Body:**
```json
{
  "user_input": "The knight entered the dark hall."
}
```
**Response:**
```json
{
  "story": "As the knight stepped forward...",
  "ended": false
}
```

### 📌 `POST /end_story`
**Request Body:**
```json
{}
```
**Response:**
```json
{
  "story": "And they lived happily ever after...",
  "ended": true
}
```

### 📌 `POST /feedback`
**Request Body:**
```json
{
  "feedback": "like"  
}
```
**Response:**
```json
{
  "message": "Feedback received",
  "feedback_score": 1
}
```

### 📌 `GET /download_story`
📥 Downloads the generated story as a **PDF**.

---

## ⏹️ Stopping the Server
To stop the Flask server, press `CTRL + C` in the terminal.

---

## 📜 License
This project is **open-source** and free to use.

📌 *Happy Storytelling! ✨*
