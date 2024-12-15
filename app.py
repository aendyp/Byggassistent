import os
import logging
from flask import Flask, request, jsonify, render_template
from langchain_community.chat_models import ChatOpenAI
from utils.document_utils import load_documents
from utils.qa_utils import setup_openai_client, setup_conversational_chain, create_vector_store

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Last inn dokumenter og sett opp systemer
documents = load_documents()
embeddings = setup_openai_client().embeddings
vector_stores = {name: create_vector_store(docs, embeddings) for name, docs in documents.items()}
llm = setup_openai_client().llm
qa_systems = {name: setup_conversational_chain(db, llm) for name, db in vector_stores.items()}

# Samtalehistorikk
conversation_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "Ingen spørring gitt"}), 400

    global conversation_history

    # Legg til brukerens spørring
    conversation_history.append({"role": "user", "content": user_query})

    # Konverter samtalelogg til riktig format
    formatted_history = [
        (msg["content"], conversation_history[i + 1]["content"])
        for i, msg in enumerate(conversation_history[:-1])
        if msg["role"] == "user" and i + 1 < len(conversation_history)
    ]

    try:
        # Velg relevant Q&A-system basert på spørsmålet
        responses = {}
        for name, qa_system in qa_systems.items():
            responses[name] = qa_system.run({"query": user_query, "chat_history": formatted_history})

        # Legg til botens svar i samtalelogg
        conversation_history.append({"role": "assistant", "content": responses})

        return jsonify({"responses": responses})
    except Exception as e:
        logger.error(f"Feil under spørring: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Renders standardport
    print(f"Starter applikasjonen på port {port}...")
    app.run(host="0.0.0.0", port=port)
