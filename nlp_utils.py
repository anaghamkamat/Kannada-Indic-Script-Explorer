
import re
import random
import unicodedata
from collections import Counter

# --- 1. Preprocessing & Normalization ---

def normalize_kannada(text):
    """
    Normalizes Kannada text by:
    1. Removing Zero-Width Joiners (ZWJ) and Non-Joiners (ZWNJ) commonly found in Indic text.
    2. Normalizing whitespace.
    3. Basic unicode normalization (NFC).
    """
    if not text: return ""
    
    # Unicode Normalization
    text = unicodedata.normalize('NFC', text)
    
    # Remove ZWJ/ZWNJ
    text = text.replace('\u200d', '').replace('\u200c', '')
    
    # Remove typical English punctuation if needed, keeping Kannada punctuations if any
    # For now, just basic strip
    text = text.strip()
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text

def preprocess_text(text, remove_stopwords=False):
    """
    Tokenizes and optionally removes stopwords.
    """
    text = normalize_kannada(text)
    
    # Simple whitespace tokenization
    # In real world, we'd use a sentencepiece tokenizer or similar
    tokens = text.split(' ')
    
    if remove_stopwords:
        # A small sample list of Kannada stopwords
        stopwords = {
            'ಮತ್ತು', 'ಒಂದು', 'ಈ', 'ಆ', 'ನನ್ನ', 'ನಿಮ್ಮ', 'ಅವರು', 'ಇದು', 'ಆದರೆ', 
            'ಬಗ್ಗೆ', 'ನಾವು', 'ನೀವು', 'ಎಂದು', 'ಇದೆ', 'ಆಗಿ', 'ಅದು', 'ಅಲ್ಲಿ', 'ಇಲ್ಲಿ'
        }
        tokens = [t for t in tokens if t not in stopwords]
        
    return tokens

# --- 2. Classification (Rule Based) ---

def classify_text(text):
    """
    Classifies text into categories based on keyword presence.
    Categories: Sports, Politics, Cinema, Technology, General
    """
    keywords = {
        'Sports': ['ಕ್ರಿಕೆಟ್', 'ಆಟ', 'ಬ್ಯಾಟಿಂಗ್', 'ಬೌಲಿಂಗ್', 'ಪಂದ್ಯ', 'ಕ್ರೀಡೆ', 'ಗೆಲುವು', 'ಸೋಲು'],
        'Politics': ['ಚುನಾವಣೆ', 'ಸರ್ಕಾರ', 'ರಾಜಕೀಯ', 'ಮಂತ್ರಿ', 'ಪಕ್ಷ', 'ಮತದಾನ', 'ಪ್ರಧಾನಿ'],
        'Cinema': ['ಚಲನಚಿತ್ರ', 'ನಟ', 'ನಟಿ', 'ಸಿನಿಮಾ', 'ಹಾಡು', 'ನಿರ್ದೇಶಕ', 'ತೆರೆ'],
        'Technology': ['ತಂತ್ರಜ್ಞಾನ', 'ಕಂಪ್ಯೂಟರ್', 'ಮೊಬೈಲ್', 'ಜಾಲತಾಣ', 'ಸಾಫ್ಟ್ವೇರ್', 'ಅಂತರ್ಜಾಲ']
    }
    
    scores = {cat: 0 for cat in keywords}
    
    for token in text.split():
        for cat, words in keywords.items():
            if any(w in token for w in words):
                scores[cat] += 1
                
    # Get max score
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        return "General / Unclassified"
    return best_cat

# --- 3. Sentiment Analysis (Lexicon Based) ---

def analyze_sentiment(text):
    """
    Returns polarity (-1 to 1) and label.
    """
    positive_words = [
        'ಚೆನ್ನಾಗಿದೆ', 'ಸುಂದರ', 'ಉತ್ತಮ', 'ಶ್ರೇಷ್ಠ', 'ಖುಷಿ', 'ಪ್ರೀತಿ', 'ಗೆಲುವು', 'ಅದ್ಭುತ', 
        'ಒಳ್ಳೆಯ', 'ಸಂತೋಷ', 'ಆನಂದ', 'ಸೂಪರ್'
    ]
    negative_words = [
        'ಕೆಟ್ಟ', 'ಕಷ್ಟ', 'ದುಃಖ', 'ನೋವು', 'ಸೋಲು', 'ಅಸಹ್ಯ', 'ಕೋಪ', 'ಬೇಜಾರು', 'ಭಯ', 
        'ದೋಷ', 'ಸಮಸ್ಯೆ'
    ]
    
    score = 0
    words = text.split()
    for w in words:
        if any(p in w for p in positive_words):
            score += 1
        if any(n in w for n in negative_words):
            score -= 1
            
    # Normalize somewhat
    if score > 0: label = "Positive 😊"
    elif score < 0: label = "Negative 😞"
    else: label = "Neutral 😐"
    
    return label, score

# --- 4. Text Simplification (Demo) ---

def simplify_kannada(text):
    """
    Replaces complex/formal words with simpler colloquial ones.
    """
    replacements = {
        'ವಿದ್ಯಾರ್ಥಿ': 'ಮಕ್ಕಳು',       # Student -> Children (Contextual approx)
        'ಚಲನಚಿತ್ರ': 'ಸಿನಿಮಾ',        # Movie (Formal) -> Cinema
        'ಆರಕ್ಷಕ': 'ಪೊಲೀಸ್',          # Police (Formal) -> Police
        'ವೈದ್ಯ': 'ಡಾಕ್ಟರ್',          # Doctor (Formal) -> Doctor
        'ದೂರವಾಣಿ': 'ಫೋನ್',           # Telephone -> Phone
        'ಗ್ರಂಥಾಲಯ': 'ಲೈಬ್ರರಿ',       # Library -> Library
        'ವಿಮಾನ ನಿಲ್ದಾಣ': 'ಏರ್‌ಪೋರ್ಟ್' # Airport
    }
    
    simple_text = text
    for complex_w, simple_w in replacements.items():
        simple_text = simple_text.replace(complex_w, simple_w)
        
    return simple_text

# --- 5. Data Generation (Mock) ---

def generate_story_start(prompt):
    """
    Mock story generator using predefined templates.
    """
    templates = [
        f"ಒಂದಾನೊಂದು ಕಾಲದಲ್ಲಿ, {prompt} ಎಂಬ ಊರಿನಲ್ಲಿ ಒಬ್ಬ ರಾಜನಿದ್ದನು. ಅವನು ತುಂಬಾ ಒಳ್ಳೆಯವನು...",
        f"ಮುಂಜಾನೆ ಎದ್ದ ಕೂಡಲೇ {prompt} ನೋಡಿದ ರವಿಗೆ ಆಶ್ಚರ್ಯವಾಯಿತು! ಏಕೆಂದರೆ...",
        f"{prompt} ವಿಷಯದ ಬಗ್ಗೆ ಹೇಳಬೇಕೆಂದರೆ, ಅದು ತುಂಬಾ ಆಸಕ್ತಿದಾಯಕವಾಗಿದೆ. ನೂರಾರು ವರ್ಷಗಳ ಹಿಂದೆ..."
    ]
    return random.choice(templates)

# --- 6. Translation (Mock Dictionary) ---

def basic_translate_en_kn(text):
    """
    Very basic word-level dictionary lookup.
    """
    dictionary = {
        'hello': 'ನಮಸ್ಕಾರ',
        'world': 'ಪ್ರಪಂಚ',
        'love': 'ಪ್ರೀತಿ',
        'kannada': 'ಕನ್ನಡ',
        'good': 'ಒಳ್ಳೆಯ',
        'morning': 'ಮುಂಜಾನೆ/ಶುಭೋದಯ',
        'is': 'ಇದೆ',
        'beautiful': 'ಸುಂದರ',
        'name': 'ಹೆಸರು',
        'my': 'ನನ್ನ'
    }
    
    words = text.lower().replace('.', '').split()
    translated = []
    for w in words:
        translated.append(dictionary.get(w, w)) # Return original if not found
        
    return " ".join(translated)
