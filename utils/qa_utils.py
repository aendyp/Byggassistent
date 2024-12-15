from langchain.chains import create_retrieval_chain
from langchain.retrievers.history_aware import create_history_aware_retriever
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
        logger.info("Setter opp History Aware Retriever og Retrieval Chain.")
        
        # Opprett History Aware Retriever
        retriever = create_history_aware_retriever(
            retriever=vectorstore.as_retriever(),
            max_history=5  # Antall meldinger i historikken som skal huskes
        )
        
        # Opprett Retrieval Chain
        chain = create_retrieval_chain(
            retriever=retriever,
            llm=llm
        )
        
        return chain
    except Exception as e:
        logger.error(f"Feil under oppsett av Retrieval Chain: {e}")
        raise
