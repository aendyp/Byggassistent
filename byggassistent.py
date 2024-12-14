# Importer nødvendige biblioteker
import os
import logging
from flask import Flask, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

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
    return ChatOpenAI(openai_api_key=api_key, temperature=0)

# Last opp og prosesser dokumentene
def load_documents():
    try:
        logger.info("Laster inn dokumenter...")
        loader_tek17 = PyPDFLoader("TEK17.pdf")
        loader_pbl = PyPDFLoader("PBL.pdf")
        loader_aml = PyPDFLoader("AML.pdf")
        loader_sak10 = PyPDFLoader("SAK10.pdf")
        loader_dok = PyPDFLoader("DOK.pdf")
        loader_bhf = PyPDFLoader("BHF.pdf")
        loader_breeam = PyPDFLoader("BREEAM-NOR-v6.1.1.pdf")
        loader_avfall = PyPDFLoader("Avfallsforskriften.pdf")
        loader_byggherre = PyPDFLoader("Byggherreforskriften.pdf")
        loader_internkontroll = PyPDFLoader("Internkontrollforskriften.pdf")
        loader_forurensning = PyPDFLoader("Forurensningsloven.pdf")
        loader_arbeidsplass = PyPDFLoader("Arbeidsplassforskriften.pdf")
        loader_arbeid = PyPDFLoader("Forskrift_om_utførelse_av_arbeid.pdf")

        docs_tek17 = loader_tek17.load_and_split()
        docs_pbl = loader_pbl.load_and_split()
        docs_aml = loader_aml.load_and_split()
        docs_sak10 = loader_sak10.load_and_split()
        docs_dok = loader_dok.load_and_split()
        docs_bhf = loader_bhf.load_and_split()
        docs_breeam = loader_breeam.load_and_split()
        docs_avfall = loader_avfall.load_and_split()
        docs_byggherre = loader_byggherre.load_and_split()
        docs_internkontroll = loader_internkontroll.load_and_split()
        docs_forurensning = loader_forurensning.load_and_split()
        docs_arbeidsplass = loader_arbeidsplass.load_and_split()
        docs_arbeid = loader_arbeid.load_and_split()

        return {
            "TEK17": docs_tek17,
            "PBL": docs_pbl,
            "AML": docs_aml,
            "SAK10": docs_sak10,
            "DOK": docs_dok,
            "BHF": docs_bhf,
            "BREEAM": docs_breeam,
            "Avfall": docs_avfall,
            "Byggherre": docs_byggherre,
            "Internkontroll": docs_internkontroll,
            "Forurensning": docs_forurensning,
            "Arbeidsplass": docs_arbeidsplass,
            "Arbeid": docs_arbeid
        }
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

# Sett opp et samtalebasert Q&A-system
def setup_conversational_chain(db, llm):
    try:
        logger.info("Setter opp samtalebasert Q&A-system...")
        return ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever(), return_source_documents=False)
    except Exception as e:
        logger.error(f"Feil under oppsett av Q&A-system: {e}")
        raise

# Initialiser Q&A-systemer
documents = load_documents()
embeddings = OpenAIEmbeddings()
vector_stores = {name: create_vector_store(docs, embeddings) for name, docs in documents.items()}
llm = setup_openai_client()
qa_systems = {name: setup_conversational_chain(db, llm) for name, db in vector_stores.items()}

# Opprett en samtalelog
conversation_history = []

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
            <p>Stille et spørsmål relatert til byggetekniske forskrifter, lover og standarder, og få svar!</p>
            <textarea id="query" placeholder="Skriv spørsmålet ditt her..."></textarea>
            <button onclick="sendQuery()">Send</button>
            <div id="response" class="response"></div>
        </div>
        <script>
            async function sendQuery() {
                const query = document.getElementById('query').value;
                if (!query) {
                    alert('Vennligst skriv et spørsmål.');
                    return;
                }
                const responseDiv = document.getElementById('response');
                try {
                    const response = await fetch('/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query }),
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP-feil! Status: ${response.status}`);
                    }
                    const data = await response.json();
                    if (data.error) {
                        responseDiv.innerHTML += `<div>Error: ${data.error}</div>`;
                    } else {
                        responseDiv.innerHTML += `<div><strong>Du:</strong> ${data.query}</div>`;
                        responseDiv.innerHTML += `<div><strong>Byggassistent:</strong> ${data.response}</div>`;
                    }
                } catch (err) {
                    responseDiv.innerHTML += `<div>En feil oppstod: ${err.message}</div>`;
                }
                responseDiv.scrollTop = responseDiv.scrollHeight;
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

    global conversation_history

    conversation_history.append({"role": "user", "content": user_query})

    try:
        # Velg relevant Q&A-system basert på spørsmålet
        responses = {}
        for name, qa_system in qa_systems.items():
            responses[name] = qa_system.run({"query": user_query, "chat_history": conversation_history})

        conversation_history.append({"role": "assistant", "content": responses})
        return jsonify({
            "query": user
