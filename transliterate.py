
import sys

def get_transliteration_map():
    # Basic mapping for Kannada
    # Only covering common combinations for demonstration
    
    # Vowels (Independent)
    vowels = {
        'aa': 'ಆ', 'a': 'ಅ', 
        'ii': 'ಈ', 'i': 'ಇ', 
        'uu': 'ಊ', 'u': 'ಉ',
        'e': 'ಎ', 'ee': 'ಏ', 'ai': 'ಐ',
        'o': 'ಒ', 'oo': 'ಓ', 'au': 'ಔ',
        'am': 'ಅಂ', 'ah': 'ಅಃ'
    }
    
    # Consonants 
    # Key is English, Value is tuple (Base Char, Halant Form if available)
    # Actually, simpler to map Consonant+Vowel combos or use logic
    
    # Let's define base consonants with Halant (Virama) implied if no vowel follows
    # Kannada letter 'ka' is 0C95. 'k' (half) is 'ಕ್' (0C95 + 0CCD)
    
    consonants = {
        'k': 'ಕ್', 'kh': 'ಖ್', 'g': 'ಗ್', 'gh': 'ಘ್', 'ng': 'ಙ್',
        'ch': 'ಚ್', 'chh': 'ಛ್', 'j': 'ಜ್', 'jh': 'ಝ್', 'ny': 'ಞ್',
        't': 'ಟ್', 'th': 'ಠ್', 'd': 'ಡ್', 'dh': 'ಢ್', 'n': 'ಣ್',
        'th': 'ತ್', 'd': 'ದ್', 'dh': 'ಧ್', 'n': 'ನ್', # Overlap 'th'/'d' - standard transliteration issues
        'p': 'ಪ್', 'ph': 'ಫ್', 'b': 'ಬ್', 'bh': 'ಭ್', 'm': 'ಮ್',
        'y': 'ಯ್', 'r': 'ರ್', 'l': 'ಲ್', 'v': 'ವ್', 'w': 'ವ್',
        'sh': 'ಶ್', 'shh': 'ಷ್', 's': 'ಸ್', 'h': 'ಹ್', 'l': 'ಳ್'
    }
    
    # Vowel Signs (Matras) - added to base consonant
    # 'k' + 'a' -> 'ಕ' (remove halant). 'k'+'aa' -> 'ಕಾ'
    matras = {
        'a': '', # Inherent vowel, removes halant
        'aa': 'ಾ', 'i': 'ಿ', 'ii': 'ೀ', 
        'u': 'ು', 'uu': 'ೂ', 'ru': 'ೃ',
        'e': 'ೆ', 'ee': 'ೇ', 'ai': 'ೈ',
        'o': 'ೊ', 'oo': 'ೋ', 'au': 'ೌ',
    }
    
    return vowels, consonants, matras

def transliterate(text):
    vowels, consonants, matras = get_transliteration_map()
    result = ""
    i = 0
    n = len(text)
    
    while i < n:
        # Check for consonant matches (longest first)
        match_c = None
        len_c = 0
        for width in [3, 2, 1]:
            chunk = text[i:i+width].lower()
            if chunk in consonants:
                match_c = chunk
                len_c = width
                break
        
        if match_c:
            # We found a consonant. Check the NEXT char for vowel
            cons_halant = consonants[match_c] # e.g. 'ಕ್'
            base_cons = cons_halant[:-1] # Remove halant '್' (Unicode 0CCD) to get base? 
            # Wait, 'ಕ್' is two chars: 0C95 + 0CCD. Removing last char gives 0C95 'ಕ' (which has 'a')
            # Actually, standard logic:
            # 'ಕ್' is \u0C95\u0CCD. 
            # If followed by 'a', result is \u0C95.
            # If followed by 'aa', result is \u0C95\u0CBE.
            
            base_char = cons_halant[0] # The main letter
            
            i += len_c
            
            # Look ahead for vowel
            match_v = None
            len_v = 0
            for width in [2, 1]:
                if i + width <= n:
                    v_chunk = text[i:i+width].lower()
                    if v_chunk in matras:
                        match_v = v_chunk
                        len_v = width
                        break
            
            if match_v:
                # Apply matra
                matra = matras[match_v]
                result += base_char + matra
                i += len_v
            else:
                # No vowel, keep halant
                result += cons_halant
                
        else:
            # Check for independent vowel (at start of word or after space/vowel)
            match_ind_v = None
            len_ind_v = 0
            for width in [2, 1]:
                chunk = text[i:i+width].lower()
                if chunk in vowels:
                    match_ind_v = chunk
                    len_ind_v = width
                    break
            
            if match_ind_v:
                result += vowels[match_ind_v]
                i += len_ind_v
            else:
                # Unknown, just keep it
                result += text[i]
                i += 1
                
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(f"Input: {text}")
        print(f"Kannada: {transliterate(text)}")
    else:
        print("Provide text to transliterate.")
        print("Example: python transliterate.py namaskara")
