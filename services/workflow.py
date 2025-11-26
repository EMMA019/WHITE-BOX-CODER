from .llm_client import GeminiClient
from utils.cleaner import clean_ai_code_response
from typing import Dict
import logging
import re

logger = logging.getLogger(__name__)

EVO_CONSTITUTION = """
[EVO CONSTITUTION / COMPLIANCE & ARCHITECTURE RULES]

1. **NO IP INFRINGEMENT**: 
   - Do NOT use trademarked names (e.g., Mario, Pokemon, Disney). Use generic terms.

2. **SECURITY FIRST**: 
   - Avoid hardcoded secrets, infinite loops, or dangerous file operations.

3. **PYTHON/FLASK ARCHITECTURE (CRITICAL)**:
   - **BLUEPRINTS**: Always use Flask Blueprints for routes. NEVER put routes directly in `app.py`.
   - **EXTENSIONS**: Define `db = SQLAlchemy()` in a separate `extensions.py` to prevent circular imports.
   - **APP FACTORY**: Use `create_app()` pattern in `__init__.py` or `app.py`.

4. **FRONTEND ARCHITECTURE**:
   - **NO BUILD TOOLS**: Use Vue 3 (Composition API) and Tailwind CSS via CDN. No `npm install`.
   - **MODULARITY**: Structure code into components if possible, even in a single HTML file.

5. **ROBUSTNESS**: 
   - Always include error handling (try-except/try-catch) for API calls and DB operations.
"""

class CodeGenerationWorkflow:
    """
    Orchestrates the code generation pipeline using a Single-Shot Chain of Thought.
    Integrated with Evo's Compliance Logic.
    """
    def __init__(self, client: GeminiClient) -> None:
        self.llm_client = client

    def execute(self, prompt: str, language: str) -> Dict[str, str]:
        logger.info(f"Starting single-shot workflow for language: {language}")

        # Single, comprehensive prompt with Evo Constitution
        full_prompt = (
            f"You are an expert {language} programmer adhering to the Evo Constitution.\n\n"
            f"{EVO_CONSTITUTION}\n\n"
            f"Perform the following steps sequentially in a single response:\n"
            f"1. **Generate**: Create the initial code for the task: {prompt}\n"
            f"2. **Architecture & Safety Review**: Check if the code follows the Evo Constitution (Blueprints, Circular Imports, IP checks). List specific violations.\n"
            f"3. **Fix & Finalize**: Rewrite the code to fix violations. Ensure Flask apps use Blueprints and extensions.py pattern.\n\n"
            f"Use the following separators strictly to structure your response:\n"
            f"===INITIAL_CODE===\n"
            f"[Put initial code here]\n"
            f"===REVIEW===\n"
            f"[Put review notes here]\n"
            f"===FINAL_CODE===\n"
            f"[Put final compliant code here]"
        )

        response_text = self.llm_client.generate_content(full_prompt)
        
        # Parse the sections
        initial_code = self._extract_section(response_text, "===INITIAL_CODE===", "===REVIEW===")
        review_notes = self._extract_section(response_text, "===REVIEW===", "===FINAL_CODE===")
        final_code = self._extract_section(response_text, "===FINAL_CODE===", "$") # End of string

        # Clean codes
        initial_code = clean_ai_code_response(initial_code)
        final_code = clean_ai_code_response(final_code)

        # Fallback if final code is empty (rare case safety)
        if not final_code and initial_code:
            final_code = initial_code
            review_notes += "\n(Warning: Auto-fix failed, reverting to initial draft.)"

        return {
            "initialCode": initial_code,
            "reviewNotes": review_notes,
            "finalCode": final_code
        }

    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> str:
        """Extracts text between two markers."""
        try:
            start_idx = text.find(start_marker)
            if start_idx == -1:
                return "" # Marker not found
            
            content_start = start_idx + len(start_marker)
            
            if end_marker == "$":
                content = text[content_start:]
            else:
                end_idx = text.find(end_marker, content_start)
                if end_idx == -1:
                    content = text[content_start:] # Take rest if end marker missing
                else:
                    content = text[content_start:end_idx]
            
            return content.strip()
        except Exception:
            return ""