from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Depends, Header
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import easyocr
from PIL import Image
import io
import numpy as np
import cv2

load_dotenv()

# EasyOCR – works perfectly on Render (no Tesseract needed)
reader = easyocr.Reader(['en'], gpu=False)

app = FastAPI(
    title="Receipt Analyzer Pro – Render-Ready Version",
    description="Production AI API – OCR + JSON extraction",
    version="1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# API KEY PROTECTION
API_KEY = "sakib-receipt-secret-2025"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
async def home():
    return {"message": "Receipt Analyzer API is LIVE! Go to /docs"}

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

    contents = await file.read()
    
    # Convert bytes to numpy array for EasyOCR
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # EasyOCR – extracts text perfectly
    ocr_result = reader.readtext(image, detail=0, paragraph=True)
    ocr_text = "\n".join(ocr_result)

    if len(ocr_text.strip()) < 10:
        return {"error": "No text detected in image"}

    prompt = PromptTemplate.from_template("""
    Extract receipt data from this text and return ONLY valid JSON:
    {text}

    JSON format:
    {{
      "shop_name": "string or null",
      "date": "YYYY-MM-DD or null",
      "total_amount": number,
      "currency": "USD or null",
      "items": [
        {{"name": "string", "price": number, "category": "Food|Electronics|Clothing|Other"}}
      ]
    }}
    If unsure, use null or best guess.
    """)

    chain = prompt | llm
    response = chain.invoke({"text": ocr_text})

    import json
    try:
        data = json.loads(response.content)
    except:
        data = {"error": "JSON parse failed", "raw_ocr": ocr_text[:1000]}

    return {
        "type": "POST (protected)",
        "filename": file.filename,
        "ocr_text_preview": ocr_text[:200] + "...",
        "result": data
    }

@app.get("/receipt/{id}/status")
async def receipt_status(id: int):
    return {"receipt_id": id, "status": "processed", "total": 129.99}
