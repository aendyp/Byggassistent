# Importer nødvendige biblioteker
import os
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from openai import OpenAI

# Sett opp OpenAI-klient
def setup_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API-nøkkel mangler! Sett OPENAI_API_KEY som miljøvariabel.")
    return OpenAI(api_key=api_key)

# Last opp og prosesser dokumentene
def load_documents():
    loader_tek17 = PyPDFLoader("TEK17.pdf")
    loader_pbl = PyPDFLoader("PBL.pdf")
    docs_tek17 = loader_tek17.load_and_split()
    docs_pbl = loader_pbl.load_and_split()
    return docs_tek17, docs_pbl

# Opprett en vektormodell for søk
def create_vector_store(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)

# Sett opp et Q&A-system
def setup_qa_system(db, llm):
    return RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# Hovedfunksjon for spørringer
def main():
    print("Laster inn dokumenter...")
    docs_tek17, docs_pbl = load_documents()

    print("Oppretter vektorbutikker...")
    embeddings = OpenAIEmbeddings()
    db_tek17 = create_vector_store(docs_tek17, embeddings)
    db_pbl = create_vector_store(docs_pbl, embeddings)

    print("Setter opp Q&A-systemer...")
    llm = setup_openai_client()
    qa_tek17 = setup_qa_system(db_tek17, llm)
    qa_pbl = setup_qa_system(db_pbl, llm)

    # Eksempelspørsmål
    query = "Hva er kravene til rømning ved brann i boliger?"
    print("Spørsmål: ", query)

    response_tek17 = qa_tek17.run(query)
    response_pbl = qa_pbl.run(query)

    print("\nSvar fra TEK17:")
    print(response_tek17)

    print("\nSvar fra PBL:")
    print(response_pbl)

if __name__ == "__main__":
    main()
