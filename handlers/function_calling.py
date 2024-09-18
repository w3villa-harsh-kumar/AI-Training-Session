import aiohttp
import base64
import aiofiles
import openai
import json
import requests
# Define constants (You'll need to provide these)

class FunctionCalling:
    pass
    
    def generate_questions_handler(self, category= "Sports"):
        try:
            prompt = f"""
            You are an expert question generator, specialized in creating educational multiple-choice questions. 
            Your task is to generate a set of 2 multiple-choice questions for the category: {category}.

            Follow these guidelines:

            1. Create questions that cover a range of difficulty levels, from easy to challenging.
            2. Ensure that the questions are factual, clear, and unambiguous.
            3. Provide four distinct options for each question, labeled a, b, c, and d.
            4. Make sure that only one option is correct, and the others are plausible but incorrect.
            5. The correct answer should not follow any obvious pattern across questions.
            6. Assign a difficulty level to each question: "low", "medium", or "high".
            7. Assign marks to each question based on its difficulty: 1 for low, 1.5 for medium, 2 for high.

            For each question, provide the following information in this exact format:

            ```json
            {{
                "question": "The full text of the question goes here?",
                "a": "First option",
                "b": "Second option",
                "c": "Third option",
                "d": "Fourth option",
                "answer": "a",
                "difficulty": "medium",
                "mark": 1.5
            }}
            ```

            Remember:
            - The "answer" field should contain only the letter (a, b, c, or d) corresponding to the correct option.
            - The "difficulty" field should be one of "low", "medium", or "high".
            - The "mark" field should be 1 for low difficulty, 1.5 for medium difficulty, and 2 for high difficulty.
            - Ensure that each question and its options are factually accurate and appropriate for the given category.
            - Avoid repetitive or overly similar questions.
            - Double-check that the correct answer is indeed correct and unambiguous.
            - Provide a mix of difficulty levels across the 50 questions.
            - Must be provided a 50 questions.

            Now, please generate 2 multiple-choice questions for the category: {category}. 
            Provide your response as a valid JSON array of question objects.
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant specialized in generating multiple-choice questions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            response = FunctionCalling().openAiRequestWithFunctionCalling(messages)
            return response

        except Exception as e:
            print(f'Error in generating questions handler: {str(e)}')
            raise Exception("Failed to generate questions")


    def openAiRequestWithFunctionCalling(self, messages):
        try:
            # Define the payload for the OpenAI API request
            payload = {
                "model": "gpt-4",
                "messages": messages,
                "functions": [
                    {
                        "name": "generate_questions",
                        "description": "Generate multiple choice questions",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "questions": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "question": {"type": "string"},
                                            "a": {"type": "string"},
                                            "b": {"type": "string"},
                                            "c": {"type": "string"},
                                            "d": {"type": "string"},
                                            "answer": {"type": "string", "enum": ["a", "b", "c", "d"]},
                                            "difficulty": {"type": "string", "enum": ["low", "medium", "high"]},
                                            "mark": {"type": "number", "enum": [1, 1.5, 2]}
                                        },
                                        "required": ["question", "a", "b", "c", "d", "answer", "difficulty", "mark"]
                                    }
                                }
                            },
                            "required": ["questions"]
                        }
                    }
                ],
                "function_call": {"name": "generate_questions"}
            }

            # Set the headers for the request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            }

            print(":::Fetch the details from the openai:::")
            # Make the POST request to the OpenAI API
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                data=json.dumps(payload)
            )

            # Raise an exception if the request failed
            response.raise_for_status()

            # Extract the function call from the response
            function_call = response.json()['choices'][0]['message'].get('function_call')
            
            if function_call and function_call['name'] == "generate_questions":
                # Parse the arguments containing the questions data
                questions_data = json.loads(function_call['arguments'])
                return questions_data['questions']
            else:
                raise Exception('Unexpected response format from OpenAI')

        except requests.exceptions.RequestException as e:
            print(f"Error making request to OpenAI: {str(e)}")
            raise Exception("Failed to get response from OpenAI.")
