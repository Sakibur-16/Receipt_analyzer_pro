from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Depends, Header
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Receipt Analyzer Pro – Protected & Live",
    description="Production-ready receipt AI API with API key protection",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# API KEY PROTECTION
API_KEY = os.getenv("API_KEY", "sakib-receipt-secret-2025")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
async def home():
    return {
        "message": "Receipt Analyzer API is LIVE",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/quick-insight")
async def quick_insight(text: str = Query(..., description="Any text for AI")):
    prompt = PromptTemplate.from_template("Give 3 short bullet points about: {text}")
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return {"type": "GET", "input": text, "response": result.content}

@app.post("/analyze-receipt")
async def analyze_receipt(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files allowed")

    # TEMPORARY: Using Vision API instead of OCR
    import base64
    contents = await file.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    
    from langchain_core.messages import HumanMessage
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": """Extract receipt information from this image. Return ONLY valid JSON with no markdown, no explanation:
{"shop_name": "store name or empty string", "date": "YYYY-MM-DD or null", "total_amount": 0.00, "items": [{"name": "item", "price": 0.00}]}"""},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            }
        ]
    )
    
    try:
        response = llm.invoke([message])
        import json
        import re
        
        # Extract JSON from response (handles markdown code blocks)
        content = response.content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        
        if json_match:
            data = json.loads(json_match.group())
        else:
            # If no JSON found, return raw text
            data = {
                "raw_text": content,
                "note": "Could not parse as JSON - showing raw response"
            }
    except Exception as e:
        data = {
            "error": str(e),
            "raw_response": response.content if 'response' in locals() else "No response",
            "note": "Using Vision API - parsing failed"
        }

    return {
        "type": "POST (protected, vision-based)", 
        "filename": file.filename, 
        "result": data
    }

@app.get("/receipt/{id}/status")
async def receipt_status(id: int):
    return {"receipt_id": id, "status": "processed", "total": 129.99}
