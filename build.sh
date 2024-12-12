#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download nb_core_news_sm --direct-download
