from typing import Type

def clean_ai_code_response(text: str) -> str:
    """
    Removes markdown code block fences from AI-generated code.

    This utility handles common markdown formats like:
    - ```python ... ```
    - ``` ... ```

    Args:
        text: The raw string response from the AI model.

    Returns:
        The cleaned code string without markdown fences.
    """
    if not isinstance(text, str):
        # Return as-is if the input is not a string, for safety.
        return text

    cleaned_text = text.strip()
    lines = cleaned_text.split('\n')

    # Remove the first line if it's a code block fence (e.g., ```python or ```)
    if lines and lines[0].strip().startswith('```'):
        lines.pop(0)

    # Remove the last line if it's a code block fence
    if lines and lines[-1].strip() == '```':
        lines.pop()

    return '\n'.join(lines)
