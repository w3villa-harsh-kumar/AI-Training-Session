import aiohttp
import base64
import aiofiles

class ImageProcessor:
    pass
    async def image_info_extraction(self, image_path):
        SYSTEM_PROMPT = f"""Analyze the image provided by the user and describe it in detail. Include key visual elements such as objects, colors, people, environment, and any notable features. Ensure the description is clear, concise, and captures the essence of the image. Do not include any extra thoughts or unrelated information, just focus on the visual details of the image."""
        print("\n Image path:", image_path)
        base64_image = await ImageProcessor().encode_image_async(image_path)
        print("\n base64_image::", base64_image)
        headers = {
            'Authorization': f'Bearer sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        }
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://api.openai.com/v1/chat/completions', headers=headers, json=payload) as response:
                response.raise_for_status()
                feedback = await response.json()
                return feedback['choices'][0]['message']['content'].strip()

    

    async def encode_image_async(self, image_path):
        async with aiofiles.open(image_path, 'rb') as image_file:
            image_data = await image_file.read()
        return base64.b64encode(image_data).decode('utf-8')

