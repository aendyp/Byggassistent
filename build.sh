#!/bin/bash
# Opprett et virtuelt miljø
python3 -m venv venv
source venv/bin/activate

# Installer nødvendige Python-pakker
pip install -r requirements.txt

# Last ned spaCy-modellen for norsk
python -m spacy download nb_core_news_sm --direct-download

# Sjekk at modellen er lastet ned
echo "Verifiserer at modellen er lastet ned..."
ls /usr/local/lib/python3.10/dist-packages/spacy/data/
