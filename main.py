from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Depends, Header
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import io
import os

load_dotenv()

# Auto-detect Tesseract (works on Windows AND Linux)
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Linux (Render) uses default path automatically

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
    return {"message": "Receipt Analyzer API is LIVE → go to /docs or /redoc"}

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
    image = Image.open(io.BytesIO(contents))
    ocr_text = pytesseract.image_to_string(image)

    prompt = PromptTemplate.from_template("""
    Extract and return ONLY valid JSON:
    {text}
    {{"shop_name": "", "date": "YYYY-MM-DD or null", "total_amount": 0, "items": [{{"name": "", "price": 0, "category": ""}}]}}
    """)

    chain = prompt | llm
    response = chain.invoke({"text": ocr_text})

    import json
    try:
        data = json.loads(response.content)
    except:
        data = {"raw_ocr": ocr_text[:1000]}

    return {"type": "POST (protected)", "filename": file.filename, "result": data}

@app.get("/receipt/{id}/status")
async def receipt_status(id: int):
    return {"receipt_id": id, "status": "processed", "total": 129.99}
