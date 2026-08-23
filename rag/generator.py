import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("gemini_api")

if not api_key:
    raise ValueError("Gemini API key not found")

client = genai.Client(api_key=api_key)

model = "gemini-3.1-flash-lite"




def generate_answer(system_prompt, user_prompt):

    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7
        )
    )

    return response.text