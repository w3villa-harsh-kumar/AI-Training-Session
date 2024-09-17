import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_image(prompt, model="dall-e-3", n=1, size="1024x1024"):
    url = "https://api.openai.com/v1/images/generations"
    api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is stored in an environment variable

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "prompt": prompt,
        "n": n,
        "size": size
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Parse and return the JSON response
        response_json = response.json()
        print(json.dumps(response_json, indent=4, sort_keys=True))
        return response_json
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    prompt = "india in 2050"
    result = generate_image(prompt)
