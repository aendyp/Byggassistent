#!/bin/bash
# Opprett et virtuelt miljø
python3 -m venv venv
source venv/bin/activate

# Installer nødvendige Python-pakker
pip install -r requirements.txt

# Last ned spaCy-modellen for norsk til en spesifikk lokal mappe
python -m spacy download nb_core_news_sm --direct-download

# Flytt modellen til en bestemt mappe i prosjektet
mkdir -p /app/models/nb_core_news_sm
mv /usr/local/lib/python3.10/dist-packages/spacy/data/nb_core_news_sm /app/models/nb_core_news_sm

# Sjekk at modellen er lastet ned og flyttet korrekt
echo "Verifiserer at modellen er flyttet..."
ls /app/models/nb_core_news_sm
