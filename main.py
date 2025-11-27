from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import io

load_dotenv()

# THIS LINE FIXES EVERYTHING ON WINDOWS
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI(
    title="Receipt Analyzer Pro – GET & POST Training API",
    description="Live example for backend team | Deploy → share → win",
    version="1.0"
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1. GET – Simple text input (WORKS)
@app.get("/quick-insight")
async def quick_insight(text: str = Query(..., description="Any text for AI")):
    prompt = PromptTemplate.from_template("Give 3 bullet points about: {text}")
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return {"type": "GET", "input": text, "response": result.content}

# 2. POST – File upload + OCR with pytesseract (WORKS ON WINDOWS)
@app.post("/analyze-receipt")
async def analyze_receipt(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files allowed")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # OCR using pytesseract (no easyocr = no Windows error)
    ocr_text = pytesseract.image_to_string(image)

    prompt = PromptTemplate.from_template("""
    Extract receipt data from this OCR text and return ONLY valid JSON:
    {text}

    Format:
    {
      "shop_name": "string or null",
      "date": "YYYY-MM-DD or null",
      "total_amount": number,
      "items": [
        {"name": "string", "price": number, "category": "Food|Electronics|Clothing|Other"}
      ]
    }
    """)

    chain = prompt | llm
    response = chain.invoke({"text": ocr_text})

    import json
    try:
        data = json.loads(response.content)
    except:
        data = {"error": "JSON parse failed", "raw_ocr": ocr_text[:1000]}

    return {
        "type": "POST with file",
        "filename": file.filename,
        "ocr_text_length": len(ocr_text),
        "result": data
    }

# 3. GET with path parameter (WORKS)
@app.get("/receipt/{id}/status")
async def receipt_status(id: int):
    return {"receipt_id": id, "status": "processed", "total": 129.99}

@app.get("/")
def home():
    return {"message": "Receipt Analyzer API is LIVE → go to /docs"}