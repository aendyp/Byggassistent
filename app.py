from flask import Flask, request, Response
import json

# Initialize Flask app
app = Flask(__name__)

# Load the TEK17 database
with open("TEK17_database.json", "r", encoding="utf-8") as f:
    database = json.load(f)

# Function to search and summarize the query
def search_and_summarize(query, database):
    results = []
    for entry in database:
        if query.lower() in entry["content"].lower():
            results.append(entry)
    if not results:
        return {"summary": "Ingen relevante avsnitt ble funnet.", "references": "Ingen"}

    # Create the summary and references
    summary = "Oppsummering:\n\n"
    references = []
    for result in results[:3]:  # Limit to the top 3 results
        summary += f"- {result['content'][:200]}...\n\n"  # Include a snippet of the content with extra spacing
        references.append(f"Side {result['page']}")
    
    return {"summary": summary.strip(), "references": ", ".join(references)}  # Format references as a single string

# Flask route to handle POST requests
@app.route("/ask", methods=["POST"])
def ask():
    # Get the query from the request
    query = request.json.get("query")
    if not query:
        return Response(
            json.dumps({"error": "Ingen forespørsel mottatt."}, ensure_ascii=False),
            content_type="application/json",
            status=400
        )

    # Get the response from the search function
    response = search_and_summarize(query, database)

    # Serialize response with proper Unicode handling
    return Response(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
