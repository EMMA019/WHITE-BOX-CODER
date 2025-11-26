import os
import time
import google.generativeai as genai
from typing import Optional

class LLMConnectionError(Exception):
    """Custom exception for errors related to the LLM API connection."""
    pass

class GeminiClient:
    """
    A client to handle all communications with the Google Gemini API.
    """
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the Gemini client and configures the API.

        Args:
            api_key: The Google Gemini API key.

        Raises:
            ValueError: If the API key is not provided or found in environment variables.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            raise ValueError("GEMINI_API_KEY is not configured. Please set it in your .env file.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction="あなたは、世界クラスの優秀なプログラマーです。あらゆるプログラミング言語に精通し、常にクリーンで効率的、そして堅牢なコードを生成します。指示がない限り、解説や追加のテキストは含めず、要求されたコードのみを出力してください。"
        )
        print("GeminiClient initialized successfully.")

    def generate_content(self, prompt_text: str) -> str:
        """
        Calls the Google Gemini API to generate content.

        Args:
            prompt_text: The prompt to send to the language model.

        Returns:
            The text response from the model.

        Raises:
            LLMConnectionError: If there is an issue communicating with the Gemini API.
        """
        try:
            print(f"--- Calling Gemini API ---")
            print(f"Prompt: {prompt_text[:150]}...")

            response = self.model.generate_content(prompt_text)

            # A small delay to avoid hitting potential rate limits in rapid succession
            time.sleep(1)

            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            # Wrap the original exception to provide more context
            raise LLMConnectionError(f"Failed to communicate with Gemini API: {e}")
