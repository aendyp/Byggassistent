import os
import logging
from flask import Flask, request, jsonify
from utils.document_utils import load_documents
from utils.qa_utils import setup_openai_client, setup_conversational_chain, create_vector_store

# Flask-app instans
app = Flask(__name__)

# Konfigurer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser Q&A-systemer
logger.info("Laster inn dokumenter...")
documents = load_documents()
logger.info("Oppretter vector store...")
embeddings = setup_openai_client().embeddings
vector_stores = {name: create_vector_store(docs, embeddings) for name, docs in documents.items()}
logger.info("Oppretter Q&A-systemer...")
llm = setup_openai_client().llm
qa_systems = {name: setup_conversational_chain(db, llm) for name, db in vector_stores.items()}

# Opprett en samtalelog
conversation_history = []

@app.route("/")
def home():
    return open("templates/index.html").read()

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
            responses[name] = qa_system.invoke({"input": user_query, "chat_history": conversation_history})

        # Gjør alle objekter i responses serialiserbare
        for name, response in responses.items():
            if isinstance(response, list):  # Håndter lister av objekter
                responses[name] = [str(obj) for obj in response]
            else:  # Håndter enkeltobjekter
                responses[name] = str(response)

        conversation_history.append({"role": "assistant", "content": responses})
        return jsonify({"responses": responses})
    except Exception as e:
        logger.error(f"Feil under spørring: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render standardport
    app.run(host="0.0.0.0", port=port)
