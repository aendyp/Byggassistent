from flask import Flask, request, Response, send_from_directory
import json
from rapidfuzz import process

app = Flask(__name__)

# Load the TEK17 database
with open("TEK17_database.json", "r", encoding="utf-8") as f:
    database = json.load(f)

# Fuzzy search and summarize function
def search_and_summarize(query, database):
    results = []
    for entry in database:
        score = process.extractOne(query, [entry["content"]])
        if score and score[1] > 70:  # Match threshold
            results.append(entry)
    if not results:
        return {"summary": "Ingen relevante avsnitt ble funnet.", "references": "Ingen"}

    summary = "Oppsummering:\n\n"
    references = []
    for result in results[:3]:  # Limit to the top 3 results
        summary += f"- {result['content'][:200]}...\n\n"
        references.append(f"Side {result['page']}")
    return {"summary": summary.strip(), "references": ", ".join(references)}

# Route for API requests
@app.route('/ask', methods=["POST"])
def ask():
    query = request.json.get("query")
    if not query:
        return Response(
            json.dumps({"error": "Ingen forespørsel mottatt."}, ensure_ascii=False),
            content_type="application/json",
            status=400
        )

    response = search_and_summarize(query, database)
    return Response(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )

# Route to serve the web interface
@app.route('/')
def home():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
