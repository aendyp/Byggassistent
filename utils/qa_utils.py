from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
import os
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
            raise ValueError("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
        logger.info("Initialiserer OpenAI-klient med gitt API-nøkkel.")
        try:
            self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0)
            self.embeddings = OpenAIEmbeddings()
        except Exception as e:
            logger.error(f"Feil under opprettelse av OpenAI-klient: {e}")
            raise

def setup_openai_client():
    return OpenAIClient()

def create_vector_store(docs, embeddings):
    try:
        logger.info("Oppretter FAISS-vector store.")
        return FAISS.from_documents(docs, embeddings)
    except Exception as e:
        logger.error(f"Feil under opprettelse av vector store: {e}")
        raise

def setup_conversational_chain(vectorstore, llm):
    try:
        logger.info("Setter opp Conversational Retrieval Chain.")
        return ConversationalRetrievalChain.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            chain_type="stuff"
        )
    except Exception as e:
        logger.error(f"Feil under oppsett av Conversational Chain: {e}")
        raise
