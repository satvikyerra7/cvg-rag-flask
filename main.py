import os
import pandas as pd
import re
import constants
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Load API key from environment variable
googleapi_key = constants.googleapi_key
genai.configure(api_key=googleapi_key)

app = Flask(__name__)

# Load CSV file from "data" folder
CSV_PATH = os.path.join(os.getcwd(), "data", "dataset.csv")

# Debugging: Print the CSV path
print(f"Loading CSV from: {CSV_PATH}")

# Check if the CSV file exists
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

# Load CSV with UTF-8 encoding
df = pd.read_csv(CSV_PATH, encoding="utf-8")

# Debugging: Print first few rows of CSV
print("CSV Data Loaded:")
print(df.head())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Debugging: Print received query
        print(f"Received query: {query}")

        # Convert query to lowercase
        query_lower = query.lower()

        # Use regex to match words in CSV
        def match_row(row):
            return any(re.search(rf"\b{re.escape(word)}\b", str(value).lower()) for word in query_lower.split() for value in row)

        matching_rows = df[df.apply(match_row, axis=1)]

        if matching_rows.empty:
            return jsonify({"response": "No relevant data found in the CSV."})

        retrieved_data = matching_rows.to_string(index=False)

        # Debugging: Print retrieved data
        print(f"Retrieved Data:\n{retrieved_data}")

        # Use retrieved data for RAG with Gemini
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Use this information to answer the question: {retrieved_data}. Now answer: {query}")

        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
