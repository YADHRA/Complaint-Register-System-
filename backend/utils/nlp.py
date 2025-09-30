import spacy
nlp = spacy.load("en_core_web_sm")
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
