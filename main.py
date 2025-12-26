import os
import uvicorn
import re
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

MY_API_KEY = os.environ.get("GENAI_API_KEY")

# Priority List: Genius -> Expert -> Fast -> Backup
MODEL_PRIORITY_LIST = [
    "gemini-3-flash",          
    "gemini-2.5-flash",        
    "gemini-2.5-flash-lite",   
    "gemma-3-27b-it",          
]

def clean_json_text(text):
    match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match: return match.group(1)
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match: return match.group(0)
    return text

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    if not MY_API_KEY:
        raise HTTPException(status_code=500, detail="Server Error: Key missing.")

    client = genai.Client(api_key=MY_API_KEY)
    last_error = None

    prompt = f"""
    Act as a strict DSA Tutor. Analyze this {request.language} code.
    Return ONLY valid JSON with keys: "time_complexity", "space_complexity", "bugs", "optimization_tips".
    Code:
    {request.code}
    """

    for model_name in MODEL_PRIORITY_LIST:
        try:
            print(f"Trying: {model_name}...") 
            response = client.models.generate_content(model=model_name, contents=prompt)
            cleaned_json = clean_json_text(response.text)
            json.loads(cleaned_json) 
            
            # SUCCESS! Return result AND the model name
            return {
                "result": cleaned_json, 
                "model_used": model_name 
            }

        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e
            continue 

    return {"result": json.dumps({
        "time_complexity": "Error",
        "bugs": f"All models failed. Last error: {str(last_error)}"
    }), "model_used": "System Overload"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
