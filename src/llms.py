import os
import time

from dotenv import load_dotenv
import openai
import google.generativeai as genai

load_dotenv()


class GoogleGemini:
    def __init__(self, model: str):
        gemini_pro = "gemini-1.5-pro"
        gemini_flash = "gemini-1.5-flash"
        self.model_name = gemini_pro if "pro" in model else gemini_flash
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)

    def chat_completion(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except ValueError:
            return "Error"
        except Exception as e:
            return f"Error: {e}"


class OpenAIGPT:
    def __init__(self, model: str):
        gpt_3 = "gpt-3.5"
        gpt_4 = "gpt-4o-mini"
        self.model_name = gpt_3 if "gpt-3" in model else gpt_4
        self.client = openai.OpenAI()

    def chat_completion(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
            completion_text = response.choices[0].message.content
            return completion_text
        except Exception as e:
            print(f"Error: {e}")


class LLM:
    def __init__(self, model: str):
        self.model = GoogleGemini(model=model) if "gemini" in model else OpenAIGPT(model=model)
        self.model_name = self.model.model_name
        self.current_latency = 0
        self.answer = ""

    def record_latency(self, prompt):
        start_time = time.time()

        response = self.model.chat_completion(prompt=prompt)
        # Record the end time
        end_time = time.time()

        # Calculate the latency
        latency = end_time - start_time

        return latency, response
