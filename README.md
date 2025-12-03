# 🥘 Rasoi AI - The Desi Chef

**A Context-Aware Generative AI Culinary Consultant**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Gemini API](https://img.shields.io/badge/AI-Gemini%20Pro-orange)
![Deployment](https://img.shields.io/badge/Deployed-Railway-success)

## 🚀 Live Demo
- **Live App:** [https://rasoi-ai-production.up.railway.app/](https://rasoi-ai-production.up.railway.app/)

---

## 📖 Overview
**Rasoi AI** is not just a recipe generator; it is an intelligent **Chef** designed to solve the daily "what to cook" dilemma. 

Unlike standard chatbots, Rasoi AI maintains **conversational state** (remembering your pantry across multiple messages), extracts **negative constraints** (e.g., "no oil"), and uses a **logic-gated workflow** to guide users from raw ingredients to a structured, cooking-ready recipe.

---

## ✨ Key Features

### 1. 🧠 Persistent State Management
Uses **Django Sessions** to maintain a live "Pantry" context. You can add ingredients over multiple messages, and the bot remembers everything without needing a heavy database setup.

### 2. 🚫 Intelligent Constraint Extraction
The bot understands exclusion. If you say *"I don't have salt,"* it intelligently flags this as a constraint and filters future suggestions accordingly.

### 3. ⚖️ Ambiguity Resolution (Flavor Intervention)
If your ingredients are ambiguous (e.g., *Rice + Milk*), the bot detects the conflict and asks: *"Would you prefer something Sweet (Kheer) or Savory (Fried Rice)?"* before proceeding.

### 4. 🔄 Implicit Intent Detection
Handles complex natural language flows like replacement: *"Actually, forget the onions, I have capsicum instead."* The system automatically clears the old item and updates the state.

### 5. 👨‍🍳 Logic-Gated Suggestions
Instead of hallucinating a recipe immediately, the AI follows a strict **Chain-of-Thought**:
`Gathering Phase` → `Suggestion Phase (3 Options)` → `Recipe Generation Phase`

---

## 🛠️ Tech Stack

- **Backend:** Python, Django (Monolith Architecture)
- **AI Model:** Google Gemini 1.5 Flash API
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite 
- **Deployment:** Railway

---

## 🔧 Local Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/rasoi-ai.git](https://github.com/YOUR_USERNAME/rasoi-ai.git)
cd rasoi-ai
````

### 2\. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Configure Environment Variables

Create a `.env` file in the `backend` folder (same level as `settings.py`) and add your Gemini API Key:

```env
GEMINI_API_KEY=your_google_api_key_here
```

### 5\. Run Migrations & Start Server

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

-----

## 📂 Project Structure

```
rasoi-ai/
├── backend/
│   ├── backend/          # Django Project Settings
│   ├── chatbot/          # Main App Logic
│   │   ├── templates/    # HTML Frontend
│   │   ├── static/       # CSS & Images
│   │   ├── views.py      # Core AI Logic & Prompt Engineering
│   │   └── urls.py       # API Routing
│   ├── manage.py
│   └── requirements.txt
└── README.md
```

-----
