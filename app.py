from flask import Flask, request, Response, render_template_string
import json
from rapidfuzz import fuzz
import spacy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load the TEK17 database
with open("TEK17_database.json", "r", encoding="utf-8") as f:
    database = json.load(f)

# Load the spaCy Norwegian language model
nlp = spacy.load("nb_core_news_sm")

# HTML template for the web interface (Norwegian version)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Byggassistent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        header {
            background: #007BFF;
            color: #fff;
            padding: 1rem 0;
            text-align: center;
        }
        main {
            max-width: 800px;
            margin: 2rem auto;
            background: #fff;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        input[type="text"] {
            width: calc(100% - 120px);
            padding: 0.5rem;
            margin-right: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 0.5rem 1rem;
            background: #007BFF;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        .response {
            margin-top: 2rem;
            padding: 1rem;
            background: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .response h3 {
            margin-top: 0;
        }
        /* Chat container */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
        }
        /* User bubble */
        .user-bubble {
            background-color: #eee;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 10px;
            align-self: flex-end;
        }
        /* Bot bubble */
        .bot-bubble {
            background-color: #007bff;
            color: white;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 10px;
            align-self: flex-start;
        }
    </style>
</head>
<body>
    <header>
        <h1>Byggassistent</h1>
    </header>
    <main>
        <p>Skriv inn spørsmålet ditt om TEK17:</p>
        <div class="chat-container" id="chat-container">
            </div>
        <form id="queryForm">
            <input type="text" id="query" name="query" placeholder="F.eks. Hva er krav til rømningsvei?" required>
            <button type="submit">Spør</button>
        </form>
    </main>
    <script>
        document.getElementById("queryForm").addEventListener("submit", async function(event) {
            event.preventDefault();
            const query = document.getElementById("query").value;
            const chatContainer = document.getElementById("chat-container");

            // Display user's question
            const userBubble = document.createElement("div");
            userBubble.classList.add("user-bubble");
            userBubble.textContent = query;
            chatContainer.appendChild(userBubble);

            try {
                const response = await fetch("/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ query })
                });

                if (response.ok) {
                    const data = await response.json();

                    // Display bot's response
                    const botBubble = document.createElement("div");
                    botBubble.classList.add("bot-bubble");
                    botBubble.innerHTML = `<h3>Svar:</h3><p><strong>Oppsummering:</strong> ${data.summary}</p><p><strong>Referanser:</strong> ${data.references}</p>`;
                    chatContainer.appendChild(botBubble);
                } else {
                    // Display error message
                    const botBubble = document.createElement("div");
                    botBubble.classList.add("bot-bubble");
                    botBubble.textContent = `Feil: ${response.status}`;
                    chatContainer.appendChild(botBubble);
                }
            } catch (error) {
                // Display error message
                const botBubble = document.createElement("div");
                botBubble.classList.add("bot-bubble");
                botBubble.textContent = `Feil: ${error.message}`;
                chatContainer.appendChild(botBubble);
            }
        });
    </script>
</body>
</html>
"""

def forbedret_sok(sporsmal, database):
    doc = nlp(sporsmal)
    nokkelord = [token.lemma_ for token in doc if not token.is_stop]

    resultater = []
    for oppføring in database:
        innhold = oppføring.get("content")
        score = fuzz.partial_ratio(sporsmal.lower(), innhold.lower())
        if score > 70:
            resultater.append((oppføring, score))

    # Sorter resultater basert på score
    resultater = sorted(resultater, key=lambda x: x[1], reverse=True)

    return resultater

def formater_svar(resultater):
    svar = ""
    referanser = []
    for oppføring, score in resultater[:3]:
        # Del innhold inn i avsnitt
        avsnitt = oppføring['content'].split('\n')

        svar += f"Side {oppføring['page']}:\n"
        for avsnitt in avsnitt:
            avsnitt = avsnitt.strip()
            if avsnitt:
                svar += f"{avsnitt}\n"
        svar += "\n"
        referanser.append(f"Side {oppføring['page']}")
    return svar.strip(), ", ".join(referanser)

# Route for API requests
@app.route('/ask', methods=["POST"])
def ask():
    try:
        query = request.json.get("query")
        if not query:
            return Response(
                json.dumps({"error": "Ingen forespørsel mottatt."}, ensure_ascii=False),
                content_type="application/json",
                status=400
            )

        resultater = forbedret_sok(query, database)
        if resultater:
            svar, referanser = formater_svar(resultater)
            response = {"summary": svar, "references": referanser}
        else:
            response = {"summary": "Ingen relevante avsnitt ble funnet.", "references": "Ingen"}

        return Response(
            json.dumps(response, ensure_ascii=False),
            content_type="application/json"
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return Response(
            json.dumps({"error": "En feil oppstod på serveren."}, ensure_ascii=False),
            content_type="application/json",
            status=500
        )

# Route to serve the web interface
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
