import json
import requests
import os
from prompts import (
    doctor_prompt,
)
from dotenv import load_dotenv

load_dotenv()

def chat_with_openai(user_question):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY") 

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": doctor_prompt.doctor_prompt
            },
            {
                "role": "user",
                "content": user_question
            },
        ],
        "stream": True,
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 0.95
    }

    response = requests.post(url, headers=headers, json=data)

    
    if response.status_code == 200:
        # Beautify the JSON response
        response_json = response.json()
        print(json.dumps(response_json, indent=4, sort_keys=True))
        
        content = response_json["choices"][0]["message"]["content"]
        print("\nContent of the response:", content)
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    user_question = input("Please enter your question: ")
    chat_with_openai(user_question)

