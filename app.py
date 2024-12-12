from flask import Flask, request, Response, send_from_directory
import json

app = Flask(__name__)

# Load the TEK17 database
with open("TEK17_database.json", "r", encoding="utf-8") as f:
    database = json.load(f)

def search_and_summarize(query, database):
    results = []
    for entry in database:
        if query.lower() in entry["content"].lower():
            results.append(entry)
    if not results:
        return {"summary": "Ingen relevante avsnitt ble funnet.", "references": "Ingen"}

    summary = "Oppsummering:\n\n"
    references = []
    for result in results[:3]:  # Limit to the top 3 results
        summary += f"- {result['content'][:200]}...\n\n"
        references.append(f"Side {result['page']}")
    return {"summary": summary.strip(), "references": ", ".join(references)}

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

@app.route('/')
def home():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
