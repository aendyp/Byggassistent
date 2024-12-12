#!/bin/bash
# Opprett et virtuelt miljø
python3 -m venv venv
source venv/bin/activate

# Installer nødvendige Python-pakker
pip install -r requirements.txt

# Last ned spaCy-modellen for norsk
python -m spacy download nb_core_news_sm --direct-download

# Alternativt kan du bruke denne linjen for å spesifisere en lokal bane hvis nedlastingen feiler
# python -m spacy link nb_core_news_sm /path/to/model/directory --force
