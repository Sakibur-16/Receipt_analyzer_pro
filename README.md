# 🧾 Smart Receipt Analyzer API

> **Production-ready AI API that extracts structured data from receipt images in under 3 seconds**

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://receipt-analyzer-pro-p6dz.onrender.com)
[![API Docs](https://img.shields.io/badge/API-Docs-blue?style=for-the-badge)](https://receipt-analyzer-pro-p6dz.onrender.com/docs)
[![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.122-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)

---

## 🚀 What This Does

Upload any receipt photo → Get back clean, structured JSON instantly.

**Perfect for:**
- 💰 Expense tracking apps
- 📊 Budgeting & personal finance tools  
- 🏢 Company reimbursement systems
- 📝 Tax preparation software
- 🛒 E-commerce analytics

> **Market Value:** This exact feature sells for **$1,500–$5,000** on Upwork/Fiverr right now.

---

## ⚡ Quick Start

### Test It Right Now (No Setup)

**Interactive Playground:**  
👉 [https://receipt-analyzer-pro-p6dz.onrender.com/docs](https://receipt-analyzer-pro-p6dz.onrender.com/docs)

**Test with cURL:**
```bash
curl -X POST \
  'https://receipt-analyzer-pro-p6dz.onrender.com/analyze-receipt' \
  -H 'x-api-key: sakib-receipt-secret-2025' \
  -F 'file=@your_receipt.jpg'
```

---

## 📊 Example Response

**Input:** Upload receipt image  
**Output:**
```json
{
  "type": "POST (protected, vision-based)",
  "filename": "receipt.jpg",
  "result": {
    "shop_name": "East Repair Inc.",
    "date": "2019-11-30",
    "total_amount": 154.06,
    "items": [
      {
        "name": "Front and rear brake cables",
        "price": 100.00
      },
      {
        "name": "New set of pedal arms",
        "price": 15.00
      },
      {
        "name": "Labor 3 hrs",
        "price": 15.00
      }
    ]
  }
}
```

---

## 🎯 API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/` | ❌ | Health check & API info |
| `GET` | `/quick-insight` | ❌ | Test AI text analysis |
| `POST` | `/analyze-receipt` | ✅ | Upload receipt → Get structured data |
| `GET` | `/receipt/{id}/status` | ❌ | Check receipt processing status |

---

## 🔐 Authentication

Protected endpoints require an API key in the header:

```bash
-H 'x-api-key: sakib-receipt-secret-2025'
```

---

## 💻 Integration Examples

### Python
```python
import requests

url = "https://receipt-analyzer-pro-p6dz.onrender.com/analyze-receipt"
headers = {"x-api-key": "sakib-receipt-secret-2025"}
files = {"file": open("receipt.jpg", "rb")}

response = requests.post(url, headers=headers, files=files)
data = response.json()

print(f"Shop: {data['result']['shop_name']}")
print(f"Total: ${data['result']['total_amount']}")
```

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('receipt.jpg'));

axios.post('https://receipt-analyzer-pro-p6dz.onrender.com/analyze-receipt', form, {
  headers: {
    ...form.getHeaders(),
    'x-api-key': 'sakib-receipt-secret-2025'
  }
})
.then(response => console.log(response.data))
.catch(error => console.error(error));
```

### Flutter/Dart
```dart
import 'package:http/http.dart' as http;
import 'dart:io';

Future<void> analyzeReceipt(File imageFile) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('https://receipt-analyzer-pro-p6dz.onrender.com/analyze-receipt'),
  );
  
  request.headers['x-api-key'] = 'sakib-receipt-secret-2025';
  request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  print(responseData);
}
```

---

## 🛠️ Tech Stack

- **Framework:** FastAPI (Python's fastest web framework)
- **AI Model:** OpenAI GPT-4o-mini with Vision API
- **Image Processing:** Pillow (PIL)
- **Deployment:** Render.com (Free tier, auto-deploys from GitHub)
- **Documentation:** Auto-generated Swagger UI + ReDoc

---

## 🏃 Run Locally

### Prerequisites
- Python 3.13+
- OpenAI API key

### Setup
```bash
# Clone the repository
git clone https://github.com/Sakibur-16/Receipt_analyzer_pro.git
cd Receipt_analyzer_pro

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Run the server
uvicorn main:app --reload
```

Server will start at: **http://127.0.0.1:8000**  
Docs available at: **http://127.0.0.1:8000/docs**

---

## 📁 Project Structure

```
Receipt_analyzer_pro/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-proj-your-key-here
API_KEY=sakib-receipt-secret-2025
```

---

## 🚀 Deployment

This project auto-deploys to Render.com on every push to `main` branch.

**To deploy your own:**
1. Fork this repository
2. Create account on [Render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repo
5. Set environment variables:
   - `OPENAI_API_KEY`
   - `API_KEY`
6. Deploy!

---

## 📈 Features Roadmap

- [x] Basic receipt extraction
- [x] API key authentication
- [x] Auto-generated documentation
- [x] Live deployment
- [ ] Rate limiting (5 requests/min)
- [ ] PDF export of receipt data
- [ ] Monthly expense summaries
- [ ] Multi-language receipt support
- [ ] Webhook notifications
- [ ] Database storage (PostgreSQL)

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📄 License

MIT License - feel free to use this in your own projects!

---

## 👨‍💻 Author

**Sakibur Rahman**  
🔗 [GitHub](https://github.com/Sakibur-16) | 💼 [LinkedIn](#) | 🌐 [Portfolio](#)

---

## 💡 Use Cases

**Real-world applications built with this API:**

1. **Expense Tracker App** - Users snap receipts, app auto-categorizes spending
2. **Corporate Reimbursement** - Employees upload receipts, finance team gets structured data
3. **Tax Preparation** - Accountants process hundreds of receipts in minutes
4. **Budget Analytics** - Analyze spending patterns across stores and categories
5. **E-commerce Research** - Track competitor pricing from physical stores

---

## 🆘 Support

Having issues? Check out:
- 📖 [API Documentation](https://receipt-analyzer-pro-p6dz.onrender.com/docs)
- 🐛 [Open an Issue](https://github.com/Sakibur-16/Receipt_analyzer_pro/issues)

---

## 🌟 Show Your Support

If this project helped you, give it a ⭐ on GitHub!

---

**Built with ❤️ using FastAPI and OpenAI**
