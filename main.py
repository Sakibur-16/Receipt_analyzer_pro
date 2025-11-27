from fastapi import FastAPI, File, UploadFile, Query, HTTPException, Depends, Header
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import easyocr
import numpy as np
import cv2

load_dotenv()

# EasyOCR – works perfectly on Render
reader = easyocr.Reader(['en'], gpu=False)

app = FastAPI(
    title="Receipt Analyzer Pro – FINAL WORKING",
    description="100% working on Render – no more errors",
    version="1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

API_KEY = "sakib-receipt-secret-2025"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.get("/")
async def home():
    return {"message": "Receipt Analyzer is 100% LIVE!"}

@app.get("/quick-insight")
async def quick_insight(text: str = Query(..., description="Any text")):
    prompt = PromptTemplate.from_template("Give 3 bullet points about: {text}")
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return {"response": result.content}

@app.post("/analyze-receipt")
async def analyze_receipt(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only images")

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # OCR
    ocr_result = reader.readtext(image, detail=0, paragraph=True)
    ocr_text = "\n".join(ocr_result)

    if not ocr_text.strip():
        return {"error": "No text found in image"}

    # FIXED INDENTATION HERE
    prompt = PromptTemplate.from_template(
        "Extract ONLY valid JSON from this receipt text:\n"
        "{text}\n\n"
        "Return JSON in this exact format:\n"
        "{{\n"
        '  "shop_name": "string or null",\n'
        '  "date": "YYYY-MM-DD or null",\n'
        '  "total_amount": number,\n'
        '  "items": [\n'
        '    {{"name": "string", "price": number, "category": "Food|Electronics|Other"}}\n'
        "  ]\n"
        "}}"
    )

    chain = prompt | llm
    response = chain.invoke({"text": ocr_text})

    import json
    try:
        data = json.loads(response.content)
    except:
        data = {"error": "Parse failed", "raw_ocr": ocr_text[:500]}

    return {
        "filename": file.filename,
        "result": data
    }
