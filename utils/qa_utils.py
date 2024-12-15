from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import os
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
            raise ValueError("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
        self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0)
        self.embeddings = OpenAIEmbeddings()

def setup_openai_client():
    return OpenAIClient()

def create_vector_store(docs, embeddings):
    try:
        logger.info("Oppretter vektorbutikk...")
        vector_store = FAISS.from_documents(docs, embeddings)
        logger.info("Vektorbutikk opprettet!")
        return vector_store
    except Exception as e:
        logger.error(f"Feil under opprettelse av vektorbutikk: {e}")
        raise

def setup_conversational_chain(vector_store, llm):
    try:
        logger.info("Setter opp Conversational Retrieval Chain...")
        conversational_chain = ConversationalRetrievalChain(
            retriever=vector_store.as_retriever(),
            llm=llm
        )
        logger.info("Conversational Retrieval Chain satt opp!")
        return conversational_chain
    except Exception as e:
        logger.error(f"Feil under oppsett av conversational chain: {e}")
        raise
