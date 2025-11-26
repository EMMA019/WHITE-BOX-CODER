White-Box AI Coder 📦✨
<img width="1627" height="842" alt="image" src="https://github.com/user-attachments/assets/8dd35fca-8449-4077-9734-5582c855c1b9" />
<img width="1869" height="953" alt="image" src="https://github.com/user-attachments/assets/f24e31f7-1c36-4ab0-985c-1535e5fbd5bb" />

White-Box AI Coder is a transparent, retro-styled code generation tool designed to visualize the AI's thought process. Unlike traditional "black box" code generators, this tool explicitly displays the three-stage workflow: Generate, Review, and Fix.

It leverages the Google Gemini API to not only write code but also self-correct and adhere to strict architectural and compliance rules (derived from the "Evo Constitution").

🌟 Key Features

👁️ Transparent Workflow: Watch as the AI drafts initial code, reviews it for bugs/security issues, and automatically applies fixes.

🧠 Chain-of-Thought Log: Expand the "White-Box Log" to read the AI's internal review notes and compare the initial draft with the final output.

🛡️ Built-in Compliance: Includes the "Evo Constitution" system prompt to prevent copyright infringement (e.g., blocking trademarked names) and enforce secure coding practices.

🎨 Retro & Warm UI: A nostalgic, typewriter-inspired interface designed with Tailwind CSS (Solarized Light theme).

⚡ Live Preview: Instantly run and visualize generated HTML/CSS/JavaScript code in a secure sandbox environment.

🚀 Single-Shot Architecture: Optimized for speed and cost-efficiency using a single API call to handle the entire generation-review-fix cycle.

⚡ Example: Self-Correction in Action

See how White-Box AI Coder transforms a simple script into a robust, architecturally sound application.

1. The Prompt

"Create a maze generator in Python."

2. Initial Draft (What the AI wrote first)

The AI initially generates a standalone script. While functional, it lacks proper structure.

import random

class MazeGenerator:
    def __init__(self, width, height):
        # ... implementation details ...
    
    def generate(self):
        # ... generation logic ...

if __name__ == "__main__":
    generator = MazeGenerator(21, 21)
    print(generator.generate())


3. AI Review & Analysis (The "White-Box" Logic)

The AI critiques its own code based on the Evo Constitution:

Violation 1: Python/Flask Architecture - Blueprints (Rule 3)
The code does not use Flask, and therefore does not define any routes using Flask Blueprints.

Violation 2: Python/Flask Architecture - Extensions (Rule 3)
The code does not define db = SQLAlchemy() in a separate extensions.py file.

Violation 3: Python/Flask Architecture - App Factory (Rule 3)
The code does not implement the create_app() pattern.

4. Final Output (After Self-Correction)

The AI automatically refactors the code into a proper Flask application structure.

project_root/app.py

import os
from flask import Flask
from extensions import db
from routes.maze_routes import maze_bp

def create_app():
    app = Flask(__name__)
    # ... config ...
    db.init_app(app)
    app.register_blueprint(maze_bp)
    return app


project_root/routes/maze_routes.py

from flask import Blueprint, Response
maze_bp = Blueprint('maze', __name__)

@maze_bp.route('/maze', methods=['GET'])
def get_maze():
    # ... generator logic ...


🛠️ Tech Stack

Backend: Python (Flask)

Frontend: Vue.js 3 (Composition API), Tailwind CSS (via CDN)

AI Model: Google Gemini 1.5 Pro / Flash

Architecture: Modular service-based design (services/, utils/)

🚀 Getting Started

Prerequisites

Python 3.8 or higher

A Google Cloud Project with the Gemini API enabled.

Installation

Clone the repository

git clone https://github.com/EMMA019/WHITE-BOX-CODER.git 
cd WHITE-BOX-CODER

Install dependencies

pip install -r requirements.txt


Set up Environment Variables
Create a .env file in the root directory and add your API key.

# .env
GEMINI_API_KEY="your_actual_api_key_here"
FLASK_ENV="development"


Run the Application

python app.py


Open in Browser
Navigate to http://localhost:5000 to start coding!

📖 How It Works

Input: You provide a task description and select the target language.

Processing (Backend):

The CodeGenerationWorkflow constructs a comprehensive prompt containing the "Evo Constitution".

It sends a request to Gemini API to Generate, Review, and Fix the code in a single pass.

The response is parsed to extract the Initial Draft, Review Notes, and Final Code.

Output (Frontend):

The final polished code is displayed with syntax highlighting.

You can expand the "White-Box Log" to see the AI's self-correction process.

For Web projects, switch to the "Live Preview" tab to see it in action immediately.

🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

📄 License

This project is open-source and available under the MIT License.
