import requests
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables (for API key if required)
load_dotenv()

# Define the Ollama API URL
ollama_url = "http://localhost:11434/api/generate"

# Create a function to interact with the Ollama API
def get_ollama_response(prompt: str, model: str = "gemma2:2b"):
    # Payload to send to the API
    payload = {
        "model": model,
        "prompt": prompt
    }

    # Send the request to the API (change headers if an API key is required)
    response = requests.post(ollama_url, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{Fore.RED}Failed to get response. Status Code: {response.status_code}")
        return {}

# Pretty-print the response
def print_pretty_response(response):
    if response:
        print(f"{Fore.GREEN}=== Ollama Model Response ===\n")
        print(f"{Fore.CYAN}Prompt: {Fore.WHITE}'{response.get('prompt')}'\n")
        print(f"{Fore.MAGENTA}Model Response:{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}{response.get('response')}")
    else:
        print(f"{Fore.RED}No valid response received.")

# Example usage
if __name__ == "__main__":
    prompt = "Explain the importance of fast language models."
    response = get_ollama_response(prompt)
    print_pretty_response(response)
