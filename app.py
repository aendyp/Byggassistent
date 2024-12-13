from flask import Flask, request, Response, render_template_string
import openai
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Configure OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    </style>
</head>
<body>
    <header>
        <h1>Byggassistent</h1>
    </header>
    <main>
        <p>Skriv inn spørsmålet ditt om TEK17, PBL eller andre standarder:</p>
        <form id="queryForm">
            <input type="text" id="query" name="query" placeholder="F.eks. Hva er krav til rømningsvei?" required>
            <button type="submit">Spør</button>
        </form>
        <div id="response" class="response" style="display: none;"></div>
    </main>
    <script>
        document.getElementById("queryForm").addEventListener("submit", async function(event) {
            event.preventDefault();
            const query = document.getElementById("query").value;
            const responseDiv = document.getElementById("response");
            responseDiv.style.display = "none";

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
                    responseDiv.style.display = "block";
                    responseDiv.innerHTML = `<h3>Svar:</h3><p>${data.answer}</p>`;
                } else {
                    responseDiv.style.display = "block";
                    responseDiv.innerHTML = `<p>Feil: ${response.status}</p>`;
                }
            } catch (error) {
                responseDiv.style.display = "block";
                responseDiv.innerHTML = `<p>Feil: ${error.message}</p>`;
            }
        });
    </script>
</body>
</html>
"""

# Function to query OpenAI GPT
def query_gpt(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error querying GPT: {e}")
        return "En feil oppstod ved forespørselen til GPT."

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

        prompt = f"Bruker spør: {query}\nSvar basert på TEK17 og PBL på norsk:"
        answer = query_gpt(prompt)
        return Response(
            json.dumps({"answer": answer}, ensure_ascii=False),
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
