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
        loader_bhf = PyPDFLoader("inndata/Byggherreforskriften.pdf")
        loader_breeam = PyPDFLoader("inndata/BREEAM-NOR-v6.1.1.pdf")
        loader_avfall = PyPDFLoader("inndata/Avfallsforskriften.pdf")
        loader_internkontroll = PyPDFLoader("inndata/Internkontrollforskriften.pdf")
        loader_forurensning = PyPDFLoader("inndata/Forurensningsloven.pdf")
        loader_arbeidsplass = PyPDFLoader("inndata/Arbeidsplassforskriften.pdf")
        loader_arbeid = PyPDFLoader("inndata/Forskrift_om_utførelse_av_arbeid.pdf")

        docs_tek17 = loader_tek17.load_and_split()
        docs_pbl = loader_pbl.load_and_split()
        docs_aml = loader_aml.load_and_split()
        docs_sak10 = loader_sak10.load_and_split()
        docs_dok = loader_dok.load_and_split()
        docs_bhf = loader_bhf.load_and_split()
        docs_breeam = loader_breeam.load_and_split()
        docs_avfall = loader_avfall.load_and_split()
        docs_internkontroll = loader_internkontroll.load_and_split()
        docs_forurensning = loader_forurensning.load_and_split()
        docs_arbeidsplass = loader_arbeidsplass.load_and_split()
        docs_arbeid = loader_arbeid.load_and_split()

        return {
            "TEK17": docs_tek17,
            "PBL": docs_pbl,
            "AML": docs_aml,
            "SAK10": docs_sak10,
            "DOK": docs_dok,
            "Byggherreforskriften": docs_bhf,
            "BREEAM": docs_breeam,
            "Avfall": docs_avfall,
            "Internkontroll": docs_internkontroll,
            "Forurensning": docs_forurensning,
            "Arbeidsplass": docs_arbeidsplass,
            "Arbeid": docs_arbeid
        }
    except Exception as e:
        logger.error(f"Feil under lasting av dokumenter: {e}")
        raise
