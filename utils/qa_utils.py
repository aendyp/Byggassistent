from langchain.prompts import PromptTemplate
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
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

def setup_prompt():
    # Oppdater PromptTemplate for å bruke én variabel
    return PromptTemplate(
        input_variables=["input"],  # Kombinert input
        template=(
            "Samtalelogg:\n{input}\n\n"
            "Hva er neste steg eller svar på brukerens spørring?"
        )
    )

def setup_conversational_chain(vectorstore, llm):
    try:
        logger.info("Setter opp History-Aware Retrieval Chain...")
        prompt = setup_prompt()
        
        # Opprett History-Aware Retriever
        history_aware_retriever = create_history_aware_retriever(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            prompt=prompt
        )

        return history_aware_retriever
    except Exception as e:
        logger.error(f"Feil under oppsett av History-Aware Retrieval Chain: {e}")
        raise
