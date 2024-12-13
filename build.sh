#!/bin/bash
# Opprett et virtuelt miljø
python3 -m venv venv
source venv/bin/activate

# Installer nødvendige Python-pakker
pip install -r requirements.txt

# Last ned spaCy-modellen for norsk og spesifiser en plassering
python -m spacy download nb_core_news_sm

# Verifiser at modellen er lastet ned og tilgjengelig
echo "Verifiserer at modellen er lastet ned..."
ls /usr/local/lib/python3.10/dist-packages/spacy/data/  # Sjekk hvor modellen er lastet ned

# Hvis modellen er funnet, flytt den til en annen katalog i prosjektet
echo "Flytter modellen til prosjektkatalogen..."
mkdir -p /app/models/nb_core_news_sm
mv /usr/local/lib/python3.10/dist-packages/spacy/data/nb_core_news_sm /app/models/nb_core_news_sm

# Sjekk om modellen er flyttet til prosjektmappen
ls /app/models/nb_core_news_sm
