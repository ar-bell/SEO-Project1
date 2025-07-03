import os
from google import genai
from google.genai import types

class GenAIClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in .env")
        self.client = genai.Client(api_key=api_key)

    def summarize(self, prompt: str) -> str:
        """
        Ask Gemini to produce a short summary of the prompt.
        """
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",           # or your chosen model ID
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            ),
        )
        return response.text.strip()
