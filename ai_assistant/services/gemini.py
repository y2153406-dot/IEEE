import os
import time

from google import genai


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=api_key)

        self.models = [
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
        ]

    def generate_response(self, prompt):
        last_error = None

        for model in self.models:
            for attempt in range(2):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )

                    return response.text

                except Exception as error:
                    last_error = error

                    if attempt == 0:
                        time.sleep(2)

        raise last_error