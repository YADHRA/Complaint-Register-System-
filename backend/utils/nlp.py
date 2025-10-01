import spacy
from spacy.cli import download
def get_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        download("en_core_web_sm")
        return spacy.load("en_core_web_sm")
nlp = get_nlp()
def categorize_complaint(text):
    categories = ['academic', 'infrastructure', 'hostel', 'transport', 'administration']
    doc = nlp(text.lower())
    for cat in categories:
        if cat in text.lower():
            return cat
        for ent in doc.ents:
            if cat in ent.text.lower():
                return cat
    return 'general'
