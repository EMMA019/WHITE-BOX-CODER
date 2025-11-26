import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Import custom modules
from services.llm_client import GeminiClient, LLMConnectionError
from services.workflow import CodeGenerationWorkflow

# Load environment variables from .env file
load_dotenv()

# --- Application Setup ---
app = Flask(__name__, template_folder='templates')
IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production'

# --- Service Initialization ---
gemini_client = None
workflow = None
initialization_error = None

try:
    # Initialize services once at startup.
    gemini_client = GeminiClient()
    workflow = CodeGenerationWorkflow(client=gemini_client)
except ValueError as e:
    # Capture error if API key is missing. The app can still run,
    # but the API endpoint will return a helpful error.
    initialization_error = str(e)
    print(f"WARNING: Application initialized with an error: {initialization_error}")


# --- API Endpoint ---
@app.route('/api/process_code', methods=['POST'])
def process_code():
    """
    API endpoint to handle the multi-step code generation workflow.
    """
    # Check if the services failed to initialize (e.g., missing API key)
    if initialization_error:
        return jsonify({"error": f"Server configuration error: {initialization_error}"}), 500

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        prompt = data.get('prompt')
        language = data.get('language', 'python')

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Delegate the entire business logic to the workflow service
        result = workflow.execute(prompt, language)

        return jsonify(result)

    except LLMConnectionError as e:
        # Catch specific errors from the LLM client
        print(f"An LLM connection error occurred: {e}")
        return jsonify({"error": "An error occurred while communicating with the AI. Please check the server logs and your API key."}), 500
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred in /api/process_code: {e}")
        return jsonify({"error": "An unexpected server error occurred. Please try again later."}), 500

# --- Frontend Serving ---
@app.route('/')
def index():
    """Serves the main Vue.js application."""
    return render_template('index.html')

# --- Main Execution ---
if __name__ == '__main__':
    # Adheres to PRODUCTION_SECURITY: Never hardcode debug=True
    app.run(host='0.0.0.0', port=5000, debug=not IS_PRODUCTION)
