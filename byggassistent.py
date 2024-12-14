# Importer nødvendige biblioteker
import os
import logging
from flask import Flask, render_template, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
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
    return render_template("index.html")

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
    app.run(host="0.0.0.0", port=5000)
