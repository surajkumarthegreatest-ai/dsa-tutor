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

# SECURITY: Get key from Environment Variable (Safe for GitHub)
MY_API_KEY = os.environ.get("GENAI_API_KEY")

def extract_json(text):
    """Helper to find JSON object inside AI response text"""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text 
    except:
        return text

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    if not MY_API_KEY:
        # This error happens if you forget to set the Key on Render
        raise HTTPException(status_code=500, detail="Server Error: GENAI_API_KEY not set in environment variables.")

    try:
        client = genai.Client(api_key=MY_API_KEY)
        
        prompt = f"""
        Act as a strict DSA Tutor. The user is a student trying to learn, so DO NOT give them the full code solution.
        Analyze this {request.language} code.
        
        Return ONLY a raw JSON object with these 4 keys:
        {{
            "time_complexity": "The Big O notation of the user's current code",
            "space_complexity": "The Space complexity",
            "bugs": "A readable HTML list (<ul><li>) of logical bugs or edge cases they missed.",
            "optimization_tips": "A readable HTML list (<ul><li>) explaining the *logic* of a better approach (e.g., 'Try using Two Pointers instead of a nested loop'). Do not write code."
        }}
        
        Code:
        {request.code}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        raw_text = response.text
        json_str = extract_json(raw_text)
        
        # Validate JSON
        try:
            json.loads(json_str) 
        except json.JSONDecodeError:
            return {"result": json.dumps({
                "time_complexity": "Error",
                "space_complexity": "Error",
                "bugs": "AI response was not valid JSON.",
                "optimization_tips": "Could not parse AI response."
            })}

        return {"result": json_str}

    except Exception as e:
        print(f"SERVER ERROR: {e}") 
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Render provides the port in an environment variable
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
