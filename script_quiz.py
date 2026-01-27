
import pandas as pd
import random

def load_data():
    try:
        return pd.read_csv("df_iso15924_scripts.tsv", sep="\t")
    except FileNotFoundError:
        print("Data file not found!")
        return None

def play_quiz():
    df = load_data()
    if df is None:
        return

    print("\n=== ISO Script Identification Quiz ===")
    print("Guess the 4-letter Code for the given Script Name.")
    print("Type 'quit' to exit.\n")
    
    score = 0
    total = 0
    
    # Filter for interesting scripts if Hard Mode
    # Let's ask user for mode
    print("Select Mode:")
    print("1. All Scripts (Easy)")
    print("2. Indian/Brahmic Scripts (hard)")
    mode = input("Choice (1/2): ").strip()
    
    if mode == '2':
        indic_codes = [
            'Brah', 'Deva', 'Knda', 'Taml', 'Telu', 'Mlym', 'Beng', 'Gujr', 
            'Guru', 'Orya', 'Sinh', 'Tibt', 'Khmr', 'Java', 'Bali', 'Newa', 
            'Gran', 'Sidd'
        ]
        pool = df[df['Code'].isin(indic_codes)].copy()
    else:
        pool = df
        
    while True:
        if pool.empty:
            print("No scripts available!")
            break
            
        row = pool.sample(1).iloc[0]
        name = row['English Name']
        code = row['Code']
        
        print(f"\nScript Name: {name}")
        guess = input("Enter 4-letter Code: ").strip()
        
        if guess.lower() == 'quit':
            break
            
        if guess.lower() == code.lower():
            print("Correct! +1 point")
            score += 1
        else:
            print(f"Wrong! The code was: {code}")
        
        total += 1
        print(f"Current Score: {score}/{total}")

    print(f"\nFinal Score: {score}/{total}")
    print("Thanks for playing!")

if __name__ == "__main__":
    play_quiz()
