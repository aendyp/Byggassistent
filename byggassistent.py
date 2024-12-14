# Importer nødvendige biblioteker
import os
import logging
from flask import Flask, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from openai import OpenAI

app = Flask(__name__)

# Konfigurer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sett opp OpenAI-klient
def setup_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
        raise ValueError("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
    return OpenAI(api_key=api_key)

# Last opp og prosesser dokumentene
def load_documents():
    try:
        logger.info("Laster inn dokumenter...")
        loader_tek17 = PyPDFLoader("TEK17.pdf")
        loader_pbl = PyPDFLoader("PBL.pdf")
        docs_tek17 = loader_tek17.load_and_split()
        docs_pbl = loader_pbl.load_and_split()
        return docs_tek17, docs_pbl
    except Exception as e:
        logger.error(f"Feil under lasting av dokumenter: {e}")
        raise

# Opprett en vektormodell for søk
def create_vector_store(docs, embeddings):
    try:
        logger.info("Oppretter vektorbutikk...")
        return FAISS.from_documents(docs, embeddings)
    except Exception as e:
        logger.error(f"Feil under oppretting av vektorbutikk: {e}")
        raise

# Sett opp et Q&A-system
def setup_qa_system(db, llm):
    try:
        logger.info("Setter opp Q&A-system...")
        return RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    except Exception as e:
        logger.error(f"Feil under oppsett av Q&A-system: {e}")
        raise

# Initialiser Q&A-systemer
docs_tek17, docs_pbl = load_documents()
embeddings = OpenAIEmbeddings()
db_tek17 = create_vector_store(docs_tek17, embeddings)
db_pbl = create_vector_store(docs_pbl, embeddings)
llm = setup_openai_client()
qa_tek17 = setup_qa_system(db_tek17, llm)
qa_pbl = setup_qa_system(db_pbl, llm)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Byggassistent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2rem; }
            .container { max-width: 600px; margin: 0 auto; }
            textarea { width: 100%; height: 100px; margin-bottom: 1rem; }
            button { padding: 0.5rem 1rem; background-color: #007BFF; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .response { margin-top: 1rem; padding: 1rem; background-color: #f1f1f1; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Byggassistent</h1>
            <p>Stille et spørsmål relatert til TEK17 eller PBL, og få svar!</p>
            <textarea id="query" placeholder="Skriv spørsmålet ditt her..."></textarea>
            <button onclick="sendQuery()">Send</button>
            <div id="response" class="response" style="display: none;"></div>
        </div>
        <script>
            async function sendQuery() {
                const query = document.getElementById('query').value;
                if (!query) {
                    alert('Vennligst skriv et spørsmål.');
                    return;
                }
                const responseDiv = document.getElementById('response');
                responseDiv.style.display = 'none';
                try {
                    const response = await fetch('/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query }),
                    });
                    const data = await response.json();
                    if (data.error) {
                        responseDiv.textContent = 'Error: ' + data.error;
                    } else {
                        responseDiv.innerHTML = `<strong>Spørsmål:</strong> ${data.query}<br>
                                                 <strong>Svar fra TEK17:</strong> ${data.response_tek17}<br>
                                                 <strong>Svar fra PBL:</strong> ${data.response_pbl}`;
                    }
                } catch (err) {
                    responseDiv.textContent = 'En feil oppstod: ' + err.message;
                }
                responseDiv.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "Ingen spørring gitt"}), 400

    try:
        response_tek17 = qa_tek17.run(user_query)
        response_pbl = qa_pbl.run(user_query)
        return jsonify({
            "query": user_query,
            "response_tek17": response_tek17,
            "response_pbl": response_pbl
        })
    except Exception as e:
        logger.error(f"En feil oppstod under behandling av spørringen: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Standard til 5000 hvis PORT ikke er satt
    logger.info(f"Starter serveren på host 0.0.0.0 og port {port}")
    app.run(host="0.0.0.0", port=port)
