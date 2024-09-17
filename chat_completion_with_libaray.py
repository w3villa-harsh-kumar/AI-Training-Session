import openai
import os
from prompts import doctor_prompt
from dotenv import load_dotenv
load_dotenv()

class ChatbotService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
            
    def get_chatbot_response(self, messages: list, model_name="gpt-4o") -> dict:
        try:
            response = openai.chat.completions.create(
                model=model_name,
                messages=messages
            )
            print(f"Response from {model_name} model: {response.choices[0].message.content}")
            return response
        except Exception as e:          
            print(f"Error: {e}")

if __name__ == "__main__":
    chatbot = ChatbotService()

    messages = [
        {"role": "system", "content": "You are a smart agent"},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]

    chatbot.get_chatbot_response(messages)