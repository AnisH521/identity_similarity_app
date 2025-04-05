# Aadhaar Document Similarity Scoring System

This project provides a system to compare two Aadhaar card (front faced) images based on both **face similarity** and **textual similarity** (Name and Date of Birth). It uses `face_recognition` for face comparison and the `Qwen2-VL` multi-modal LLM model for extracting text information directly from images.
---
## Workflow
![workflow](workflow\workflow_doc_similarity.png)
---
## Features

- Face detection and embedding-based similarity
- Vision-language inference using Qwen2-VL
- Text similarity scoring via fuzzy string matching
- Weighted final score combining face and text
- Jupyter notebook-based analysis and pipeline
- Designed for extensibility and API integration (FastAPI-ready)
---
## Tech Stack

- Python 3.10+
- face_recognition
- Transformers by Hugging Face
- Qwen/Qwen2-VL-2B-Instruct
- Matplotlib (for image visualization)
- Difflib, Regex, AST (for text parsing & comparison)
---
## Project Structure

```
identity-similarity/
├── analysis/
├── app/
│   ├── __init__.py
│   ├── main.py               
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        
│   ├── core/
│   │   ├── __init__.py
│   │   └── logger.py         
│   ├── services/
│   │   ├── __init__.py
│   │   ├── face.py           
│   │   ├── text.py           
│   │   └── score.py          
│   └── models/
│       ├── __init__.py
│       └── schemas.py        
├── requirements.txt
└── README.md
```
## Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/identity-similarity.git
cd identity-similarity
```
#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### Running the Application

Start the API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000, and the interactive API documentation at http://localhost:8000/docs.

## API Endpoints

### Compare Identity Documents

```
POST /api/compare
```

Upload two identity document images and get a comprehensive comparison report.

### Face Similarity

```
POST /api/face-similarity
```

Calculate similarity between faces in two images.

### Text Extraction

```
POST /api/text-extraction
```

Extract textual information from identity document images.

## Usage Examples

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/compare" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "image1=@/path/to/id1.jpg" \
  -F "image2=@/path/to/id2.jpg"
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/compare"

files = {
    "image1": open("path/to/id1.jpg", "rb"),
    "image2": open("path/to/id2.jpg", "rb")
}

response = requests.post(url, files=files)
print(response.json())
```

## Response Format

```json
{
  "face_score": 0.85,
  "text_score": 1.0,
  "overall_score": 0.91,
  "name_match": true,
  "dob_match": true,
  "extracted_text": {
    "document1": {
      "name": "John Doe",
      "dob": "1990-01-01"
    },
    "document2": {
      "name": "John Doe",
      "dob": "1990-01-01"
    },
    "name_match": true,
    "dob_match": true
  }
}
```

## License

[MIT](LICENSE)

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Qwen2-VL](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct)


