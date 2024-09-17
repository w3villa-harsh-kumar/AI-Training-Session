import openai
import os
from prompts import doctor_prompt
from dotenv import load_dotenv
load_dotenv()

class ChatbotService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
            
    def generate_image(self, prompt: str, size="1024x1024") -> dict:
        try:
            response = openai.images.generate(
                prompt=prompt,
                n=1,
                size=size
            )
            image_url = response.data[0].url
            print(f"Image URL: {image_url}")
            return response
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chatbot = ChatbotService()

    prompt = "A futuristic cityscape with flying cars"
    chatbot.generate_image(prompt)