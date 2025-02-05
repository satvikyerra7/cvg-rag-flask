# CSV-Based RAG with Gemini API

This is a **Flask-based Retrieval-Augmented Generation (RAG) system** that retrieves data from a **CSV file** and uses **Google's Gemini AI** to generate responses.

## 📌 Features
- Reads data from `dataset.csv`
- Uses **Pandas** for CSV search
- Generates answers using **Google Generative AI (Gemini)**
- Provides a simple **Flask web interface**

## 📌 Installation
```bash
git clone https://github.com/your-username/csv-rag-flask.git
cd csv-rag-flask
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
