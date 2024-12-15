from langchain_community.document_loaders import PyPDFLoader
import logging

logger = logging.getLogger(__name__)

def load_documents():
    try:
        logger.info("Laster inn dokumenter...")
        documents = {
            "TEK17": PyPDFLoader("inndata/TEK17.pdf").load_and_split(),
            "PBL": PyPDFLoader("inndata/PBL.pdf").load_and_split(),
            "AML": PyPDFLoader("inndata/AML.pdf").load_and_split(),
            "SAK10": PyPDFLoader("inndata/SAK10.pdf").load_and_split(),
            "DOK": PyPDFLoader("inndata/DOK.pdf").load_and_split(),
            "Byggherreforskriften": PyPDFLoader("inndata/Byggherreforskriften.pdf").load_and_split(),
            "BREEAM": PyPDFLoader("inndata/BREEAM-NOR-v6.1.1.pdf").load_and_split(),
            "Avfall": PyPDFLoader("inndata/Avfallsforskriften.pdf").load_and_split(),
            "Internkontroll": PyPDFLoader("inndata/Internkontrollforskriften.pdf").load_and_split(),
            "Forurensning": PyPDFLoader("inndata/Forurensningsloven.pdf").load_and_split(),
            "Arbeidsplass": PyPDFLoader("inndata/Arbeidsplassforskriften.pdf").load_and_split(),
            "Arbeid": PyPDFLoader("inndata/Forskrift_om_utførelse_av_arbeid.pdf").load_and_split()
        }
        return documents
    except Exception as e:
        logger.error(f"Feil under lasting av dokumenter: {e}")
        raise
