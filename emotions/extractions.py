import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean(text):
    # Rimuovi le note di regia e le indicazioni di scena
    cleaned_text = re.sub(r'\([^)]*\)', '', text)
    # Sostituisci i ritorni a capo multipli con un singolo ritorno a capo
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    # Unisci le linee che appartengono alla stessa battuta
    cleaned_text = re.sub(r'\n(?![A-Z][A-Z ]+\n)', ' ', cleaned_text)
    return cleaned_text

def characters_extraction(text):
    doc = nlp(text)
    characters = {}

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            character = ent.text.split()[0].strip().upper()
            if character in characters:
                characters[character] += 1
            else:
                characters[character] = 1


    sorted_characters = sorted(characters.items(), key=lambda x: x[1], reverse=True)
    main_characters = [character for character, conteggio in sorted_characters[:8]]
    return main_characters

def characters_sentences_extraction(text, character):
    sentences = []
    clean_text = clean(text)
    # prende la prima frase successiva al personaggio
    pattern = fr"\b{character}\b\s{{3,}}(.*?)(?=(\b[A-Z][A-Z ]+\b\s{{3,}})|$)"

    for match in re.finditer(pattern, clean_text, re.DOTALL | re.MULTILINE):
        sentence = match.group().strip()
        sentence = re.sub(fr"^{character}\s{{3,}}", "", sentence)
        doc = nlp(sentence)
        first_sentence = ""

        for sent in doc.sents:
            first_sentence = sent.text.strip()
            first_sentence = ' '.join(first_sentence.split())
            break

        sentences.append(first_sentence)
    
    # frasi salienti
    main_sentences = []
    for sentence in sentences:
        # Rimuovi le note di regia
        if "(continuing)" in sentence:
            continue

        # Analizza la frase con spaCy
        doc = nlp(sentence)

        # Controlla se la frase ha un verbo e una lunghezza minima
        if any(token.pos_ == "VERB" for token in doc) and len(doc) > 3:
            main_sentences.append(sentence)

    return main_sentences

