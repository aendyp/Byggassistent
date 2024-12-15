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
documents = load_documents()
embeddings = setup_openai_client().embeddings
vector_stores = {name: create_vector_store(docs, embeddings) for name, docs in documents.items()}
llm = setup_openai_client().llm
qa_systems = {name: setup_conversational_chain(db, llm) for name, db in vector_stores.items()}

# Opprett en samtalelog
conversation_history = []

@app.route("/")
def home():
    return open("static/index.html").read()

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "Ingen spørring gitt"}), 400

    global conversation_history

    conversation_history.append({"role": "user", "content": user_query})

    try:
        responses = {}
        for name, qa_system in qa_systems.items():
            responses[name] = qa_system.run({"question": user_query, "chat_history": conversation_history})

        conversation_history.append({"role": "assistant", "content": responses})
        return jsonify({"responses": responses})
    except Exception as e:
        logger.error(f"Feil under spørring: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
