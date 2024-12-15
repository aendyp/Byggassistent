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

        return {
            "TEK17": loader_tek17.load_and_split(),
            "PBL": loader_pbl.load_and_split(),
            "AML": loader_aml.load_and_split(),
            "SAK10": loader_sak10.load_and_split(),
            "DOK": loader_dok.load_and_split(),
            "Byggherreforskriften": loader_bhf.load_and_split(),
            "BREEAM": loader_breeam.load_and_split(),
            "Avfall": loader_avfall.load_and_split(),
            "Internkontroll": loader_internkontroll.load_and_split(),
            "Forurensning": loader_forurensning.load_and_split(),
            "Arbeidsplass": loader_arbeidsplass.load_and_split(),
            "Arbeid": loader_arbeid.load_and_split()
        }
    except Exception as e:
        logger.error(f"Feil under lasting av dokumenter: {e}")
        raise
