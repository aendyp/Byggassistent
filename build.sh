#!/bin/bash
# Opprett et virtuelt miljø
python3 -m venv venv
source venv/bin/activate

# Installer nødvendige Python-pakker
pip install -r requirements.txt

# Last ned spaCy-modellen for norsk
python -m spacy download nb_core_news_sm --direct-download

# Sjekk om modellen er lastet ned ved å liste innholdet i spacy/data
echo "Verifiserer at modellen er lastet ned..."
ls /usr/local/lib/python3.10/dist-packages/spacy/data/

# Sjekk om modellen finnes i katalogen
if [ -d "/usr/local/lib/python3.10/dist-packages/spacy/data/nb_core_news_sm" ]; then
  echo "Modellen er lastet ned og funnet."
else
  echo "Modellen ble ikke funnet!"
  exit 1
fi
