from langchain_community.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
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
        self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0)
        self.embeddings = OpenAIEmbeddings()

def setup_openai_client():
    return OpenAIClient()

def create_vector_store(docs, embeddings):
    try:
        return FAISS.from_documents(docs, embeddings)
    except Exception as e:
        logger.error(f"Feil under opprettelse av vector store: {e}")
        raise

def setup_conversational_chain(vectorstore, llm):
    try:
        return ConversationalRetrievalChain.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            chain_type="stuff"
        )
    except Exception as e:
        logger.error(f"Feil under oppsett av Conversational Chain: {e}")
        raise
