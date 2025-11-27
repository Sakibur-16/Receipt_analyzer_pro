# Smart Receipt Analyzer API  

**Live URL →** https://receipt-analyzer-pro.onrender.com  
**Swagger Docs →** https://receipt-analyzer-pro.onrender.com/docs  

A production-ready AI API that turns any receipt photo into clean, structured JSON in < 3 seconds.

Perfect for:
- Expense tracker apps
- Budgeting & personal finance tools
- Company reimbursement systems
- Tax preparation apps

Clients pay $1500–$5000 for this exact feature on Upwork/Fiverr right now.

# Smart Receipt Analyzer API  LIVE
**Live URL →** https://receipt-analyzer-pro.onrender.com  
**Interactive Docs →** https://receipt-analyzer-pro.onrender.com/docs

### Features
- POST `/analyze-receipt` → Upload receipt image → Get structured data
- GET `/quick-insight?text=...` → Simple text-to-insight (demo of GET requests)
- GET `/receipt/{id}/status` → Example of path parameters
- OCR powered by Tesseract (works perfectly on Windows + Render)
- Structured output using GPT-4o-mini
- Fully deployed & live 24/7

### Example Output (POST /analyze-receipt)
```json
{
  "type": "POST with file",
  "filename": "receipt.jpg",
  "ocr_text_length": 842,
  "result": {
    "shop_name": "Walmart Supercenter",
    "date": "2025-11-28",
    "total_amount": 87.34,
    "items": [
      {"name": "Milk 1L", "price": 3.29, "category": "Food"},
      {"name": "iPhone Charger", "price": 19.99, "category": "Electronics"},
      {"name": "T-Shirt", "price": 12.99, "category": "Clothing"}
    ]
  }
}
```
### Tech Stack

- FastAPI (fastest Python framework for APIs)
- GPT-4o-mini (OpenAI)
- pytesseract + Pillow (OCR)
- Deployed on Render.com (free tier)

### How to Use (For Backend/Flutter Devs)
```python
import requests

url = "https://receipt-analyzer-pro.onrender.com/analyze-receipt"
files = {'file': open('my_receipt.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### Local Development
```python
git clone https://github.com/yourusername/receipt-analyzer-pro.git
cd receipt-analyzer-pro
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
