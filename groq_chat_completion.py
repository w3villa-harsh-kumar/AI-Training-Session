import requests
import json
from typing import Dict, Any
from prompts.doctor_prompt import doctor_prompt
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def get_response(api_key: str, message) -> Dict[str, Any]:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": doctor_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"{Fore.RED}HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"{Fore.RED}Error occurred: {err}")
    return {}

def pretty_print_response(response: Dict[str, Any]) -> None:
    if response:
        print(f"{Fore.GREEN}=== Full Response from API ===")
        print(json.dumps(response, indent=4, ensure_ascii=False))

        # Extract and print the assistant's message content
        try:
            content = response['choices'][0]['message']['content']
            print(f"\n{Fore.YELLOW}=== Assistant's Response ===")
            print(f"{Fore.WHITE}{content}")
        except (KeyError, IndexError) as e:
            print(f"{Fore.RED}Error extracting message content: {e}")
    else:
        print(f"{Fore.RED}No response or an error occurred.")

# Example usage
if __name__ == "__main__":
    api_key = "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"
    message = "I'm having trouble optimizing my Merge Sort implementation. It's timing out on large inputs."
    
    print(f"{Fore.CYAN}Sending request to the API...{Style.RESET_ALL}")
    response = get_response(api_key, message)
    pretty_print_response(response)
