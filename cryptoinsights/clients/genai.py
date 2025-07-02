

#it keeps thowing errors, and i need to get the ai part running but just kinda forgot how lol
#can figure out tmr 
import os 
from google import genai

class GenAIClient: 
    def __init__(self):
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("GENAI_API_KEY not set in environment. :(")
        self.client = genai.Client(api_key=api_key)
    
    def summarize(self, prompt: str) -> str:
        """
        Calling the Google GenAI API (Gemini) to summarize when prompted.
        """
        response = self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
        )
        return response.text