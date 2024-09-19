import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.corcel.io/v1/chat/completions"

payload = {
    "model": "llama-3",
    "temperature": 0.1,
    "max_tokens": 500
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": os.getenv("CORCEL_API_KEY")
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)