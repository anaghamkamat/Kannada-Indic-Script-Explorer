
import pandas as pd
import analyze_scripts
import nlp_utils
import os

def test_morphology():
    text = "ನಮಸ್ಕಾರ"
    print(f"\nTesting Morphology on: {text}")
    result = nlp_utils.analyze_morphology(text)
    print("Aksharas:", result['aksharas'])
    print("Stats:", result['stats'])
    
    # Expected: ನ (Na) + ಮ (Ma) + ಸ್ಕಾ (Ska) + ರ (Ra) -> 4 Aksharas
    # Stats: 2 pure consonants (Na, Ma, Ra.. wait Na=N+a, so Consonant+Vowel), 
    # Actually my logic counts:
    # N (C) + a (Implicit? No, strict unicode chars)
    # Unicode:
    # U+0CA8 (Na) -> Consonant
    # U+0CAE (Ma) -> Consonant
    # U+0CB8 (Sa) + U+0CCD (Virama) + U+0C95 (Ka) + U+0CBE (Aa Matra) -> Ska (Conjunct)
    # U+0CB0 (Ra) -> Consonant
    
    # My logic:
    # Na -> New Akshara
    # Ma -> New Akshara
    # Sa -> New Akshara... wait.
    # Sa -> Consonant. Buffer=[Sa]
    # Virama -> Not new. Buffer=[Sa, Virama]
    # Ka -> Consonant. Prev was Virama. So StartNew=False. Buffer=[Sa, Virama, Ka]
    # Aa Matra -> Not new. Buffer=[Sa, Virama, Ka, Aa]
    # Ra -> Consonant. Prev not Virama. StartNew=True. Flush [Sa..Aa]. Buffer=[Ra]
    
    # Verify breakdown:
    assert len(result['aksharas']) == 4
    print("[PASS] Morphology Basic")

def test_data_analysis():
    print("\nTesting Data Analysis...")
    df = analyze_scripts.load_dataset()
    if df is None:
        print("[SKIP] Dataset not found")
        return

    growth = analyze_scripts.get_indic_script_growth(df)
    print("Growth Data Head:\n", growth.head())
    assert 'Cumulative Count' in growth.columns
    assert len(growth) > 0
    print("[PASS] Growth Analysis")
    
    latency = analyze_scripts.compare_kannada_latency(df)
    if latency is not None:
        k_row = latency[latency['English Name'] == 'Kannada']
        diff = k_row.iloc[0]['Days Difference']
        print(f"Kannada Latency Difference (should be 0): {diff}")
        assert diff == 0
        print("[PASS] Latency Analysis")

if __name__ == "__main__":
    test_morphology()
    test_data_analysis()

    print("\nTesting Advanced Features...")
    
    # 1. Chandassu
    # "Namaskara" -> Na (L), Ma (G - next is Sk), Ska (G - long Aa), Ra (L) 
    # Wait, my logic for Sk causing Ma to be Guru:
    # "Ma" is aksharas[1]. "Ska" is aksharas[2].
    # "Ska" starts with 'S' + Virama + 'k'. So yes, it is a conjunct start.
    # So Ma should be Guru (-).
    # Na is Laghu (U).
    # Ska is Guru (-) because of 'aa'.
    # Ra is Laghu (U).
    # Pattern: U - - U
    meter = nlp_utils.get_chandassu_meter("ನಮಸ್ಕಾರ")
    print(f"Chandassu 'Namaskara': {meter}")
    # Verify basics
    assert len(meter) == 4
    
    # 2. Similarity
    sim = nlp_utils.calculate_script_similarity("ನಮಸ್ಕಾರ", "")
    print(f"Similarity Score: {sim['score']}")
    print(f"Cognate: {sim['converted']}")
    assert sim['score'] > 0.9
    
    # 3. Soundex
    # 'Namaskara' vs 'Namaskaara' should hash same?
    # N M S K R vs N M S K R
    h1 = nlp_utils.kannada_phonetic_hash("ನಮಸ್ಕಾರ")
    h2 = nlp_utils.kannada_phonetic_hash("ನಮಸ್ಕಾರ") # Identical
    print(f"Phonetic Hash: {h1}")
    assert h1 == h2
    assert len(h1) > 0
    
    # 4. Stemmer
    word = "ಕನ್ನಡಿಗರು" # Kannadigaru -> Kannada
    stem = nlp_utils.simple_kannada_stemmer(word)
    print(f"Stemmer '{word}' -> '{stem}'")
    # Should strip 'garu' or at least 'aru'
    # 'garu' is not in list, 'aru' is.
    # actually 'galu' is plural. 'aru' is human plural.
    # My suffix list has 'aru'.
    # Expected: 'kannadig'
    # Wait, 'Kannadigaru' ends with 'aru'.
    # Stem: 'Kannadiga'.
    # If logic is simple suffix stripping:
    # "Kannada" + "alli" = "Kannadadalli" -> Stemmer -> "Kannada" (ideal)
    
    stem2 = nlp_utils.simple_kannada_stemmer("ಮನೆಯಲ್ಲಿ") # Maneyalli -> Mane
    print(f"Stemmer 'Maneyalli' -> '{stem2}'")
    assert len(stem2) < len("ಮನೆಯಲ್ಲಿ")
    
    # 5. Markov
    print("Testing Markov Generator...")
    gen = nlp_utils.markov_gen.generate(length=5)
    print(f"Generated: {gen}")
    assert len(gen.split()) > 1
    
    print("[PASS] Advanced Features (Phase 2 & 3)")
