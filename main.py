from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
from handlers.image_data_extraction import ImageProcessor
from handlers.function_calling import FunctionCalling
import aiohttp
import base64
import aiofiles
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

# Initialize the FastAPI app
app = FastAPI()

# OpenAI API key (hard-coded for this example)
OPENAI_API_KEY = 'sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Define the request body model
class QueryRequest(BaseModel):
    query: str = Field(..., title="Query", description="The query to send to the OpenAI assistant", min_length=1)

# Define the response model
class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def get_openai_response(request: QueryRequest):
    """
    Get a response from the OpenAI assistant based on the given query.

    Args:
    request: A QueryRequest object containing the query to send to the OpenAI assistant.

    Returns:
    A QueryResponse object containing the response from the OpenAI assistant.

    Raises:
    HTTPException: If the OpenAI API returns an error status code.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Your name is 'Anant'. you are a helpful assistant."},
            {"role": "user", "content": request.query}
        ]
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OPENAI_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            # Extract the response text
            openai_response = data['choices'][0]['message']['content'].strip()
            return QueryResponse(response=openai_response)
        except httpx.HTTPStatusError as e:
            print(f"HTTPStatusError: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            print(f"Exception: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))



@app.post("/extract-text")
async def extract_text(image: UploadFile = File(...)):
    """
    Extract text from an image using OpenAI's image-to-text model.

    Args:
    image: The image to extract text from, as a UploadFile.

    Returns:
    A JSONResponse containing a dictionary with a single key: "result",
    which contains the extracted text and details.

    Raises:
    HTTPException:
        If the image is not in JPG format, with a status code of 400.
        If there is an internal server error, with a status code of 500.
    """
    if image.content_type != 'image/jpeg':
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPG is supported.")
    
    try:
        # Save the image temporarily
        temp_file = f"/tmp/{image.filename}"
        async with aiofiles.open(temp_file, 'wb') as out_file:
            content = await image.read()  # Read the image file
            await out_file.write(content)  # Write the image to the temporary file
        
        # Process the image
        result = await ImageProcessor().image_info_extraction(temp_file)
        
        # Return the extracted text and details as JSON
        return JSONResponse(content={"result": result})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/function_calling")
async def extract_text():
    """
    Endpoint for calling the generate_questions_handler function of FunctionCalling class.

    Returns:
    A JSONResponse containing a dictionary with a single key: "result",
    which contains the result of calling generate_questions_handler.

    Raises:
    HTTPException:
        If there is an internal server error, with a status code of 500.
    """
    try:
        result = FunctionCalling().generate_questions_handler()
        return JSONResponse(content={"result": result})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
