from langchain_community.document_loaders import PyPDFLoader
import logging

logger = logging.getLogger(__name__)

def load_documents():
    try:
        logger.info("Laster inn dokumenter...")
        loader_tek17 = PyPDFLoader("inndata/TEK17.pdf")
        loader_pbl = PyPDFLoader("inndata/PBL.pdf")
        loader_aml = PyPDFLoader("inndata/AML.pdf")
        loader_sak10 = PyPDFLoader("inndata/SAK10.pdf")
        loader_dok = PyPDFLoader("inndata/DOK.pdf")
        loader_bhf = PyPDFLoader("inndata/BHF.pdf")

        docs_tek17 = loader_tek17.load_and_split()
        docs_pbl = loader_pbl.load_and_split()
        docs_aml = loader_aml.load_and_split()
        docs_sak10 = loader_sak10.load_and_split()
        docs_dok = loader_dok.load_and_split()
        docs_bhf = loader_bhf.load_and_split()

        return {
            "TEK17": docs_tek17,
            "PBL": docs_pbl,
            "AML": docs_aml,
            "SAK10": docs_sak10,
            "DOK": docs_dok,
            "BHF": docs_bhf
        }
    except Exception as e:
        logger.error(f"Feil under lasting av dokumenter: {e}")
        raise
