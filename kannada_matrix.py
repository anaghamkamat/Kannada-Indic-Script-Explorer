
import random
import time
import shutil
import sys

def get_kannada_char():
    # Kannada Unicode block is 0x0C80 to 0x0CFF
    # We'll pick some common letters/numbers to look cool
    # Range 0x0C85 (A) to 0x0CB9 (Ha) roughly
    code = random.randint(0x0C85, 0x0CB9)
    return chr(code)

def matrix_rain():
    # Get terminal size
    columns, rows = shutil.get_terminal_size()
    
    # Initialize drops: 0 means no drop, >0 means length of trail left
    drops = [0] * columns
    
    print("\033[2J") # Clear screen
    
    try:
        while True:
            line = ""
            for i in range(columns):
                if drops[i] == 0:
                    # Random chance to start a drop
                    if random.random() < 0.02:
                        drops[i] = random.randint(5, 20) # length of trail
                        char = get_kannada_char()
                        # Green color
                        line += f"\033[92m{char}\033[0m"
                    else:
                        line += " "
                else:
                    # Continue the drop
                    char = get_kannada_char()
                    
                    # If it's the 'head' of the drop (random chance), make it bright white/bold
                    if random.random() < 0.1:
                         line += f"\033[1;37m{char}\033[0m"
                    else:
                         line += f"\033[32m{char}\033[0m" # Darker green
                    
                    drops[i] -= 1
            
            print(line)
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\033[0m") # Reset color
        print("\nMatrix Rain stopped.")

if __name__ == "__main__":
    matrix_rain()
