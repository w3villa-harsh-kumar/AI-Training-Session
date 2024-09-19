import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from groq import Groq

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

def get_groq_response():
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY", "your_default_api_key")  # Fallback to default
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="mixtral-8x7b-32768",
    )

    return chat_completion

def print_pretty_response(chat_completion):
    try:
        response_content = chat_completion.choices[0].message.content
        
        # Print headers and content with colors
        print(f"{Fore.GREEN}=== Chat Completion Response ===\n")
        print(f"{Fore.YELLOW}System Role: {Fore.WHITE}Helpful Assistant\n")
        print(f"{Fore.CYAN}User Query: {Fore.WHITE}'Explain the importance of fast language models.'\n")
        print(f"{Fore.MAGENTA}Assistant's Response:{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}{response_content}")
        
    except (KeyError, IndexError) as e:
        print(f"{Fore.RED}Error extracting response content: {e}")

# Example usage
if __name__ == "__main__":
    chat_completion = get_groq_response()
    print_pretty_response(chat_completion)
