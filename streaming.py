import json
import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def stream_chat_completion(prompt, model="gpt-4", max_tokens=150):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is stored in an environment variable

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "stream": True  # Enable streaming
    }

    response = requests.post(url, headers=headers, json=data, stream=True)

    if response.status_code == 200:
        print("Streaming response:")
        for line in response.iter_lines():
            if line:
                # Decode line and handle the JSON response
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    content = decoded_line[len('data: '):]
                    if content != "[DONE]":
                        # Format and print content to simulate typing effect
                        content_data = json.loads(content)
                        message = content_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                        if message:
                            # Print character by character with a delay to simulate typing effect
                            for char in message:
                                print(char, end='', flush=True)
                                time.sleep(0.05)  # Adjust delay for faster/slower typing effect
                        # Optionally, you can add a newline after each message
                        print()
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Example usage
if __name__ == "__main__":
    prompt = "Explain the theory of relativity."
    stream_chat_completion(prompt)
