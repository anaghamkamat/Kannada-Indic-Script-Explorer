
import pandas as pd
import datetime

# Load the dataset
try:
    df = pd.read_csv("df_iso15924_scripts.tsv", sep="\t")
except FileNotFoundError:
    print("Error: df_iso15924_scripts.tsv not found.")
    exit()

# List of Indic/Brahmic script codes to filter
indic_scripts = [
    'Brah', 'Deva', 'Knda', 'Taml', 'Telu', 'Mlym', 'Beng', 'Gujr', 
    'Guru', 'Orya', 'Sinh', 'Tibt', 'Khmr', 'Java', 'Bali', 'Newa', 
    'Gran', 'Sidd'
]

# Filter the dataframe
df_indic = df[df['Code'].isin(indic_scripts)].copy()
df_indic['Date'] = pd.to_datetime(df_indic['Date'])
df_indic = df_indic.sort_values('Date')

print("\n--- Indian/Brahmic Script Standardization Timeline ---")
print(f"{'Date':<12} | {'Code':<5} | {'Name'}")
print("-" * 50)

for _, row in df_indic.iterrows():
    date_str = row['Date'].strftime('%Y-%m-%d')
    print(f"{date_str:<12} | {row['Code']:<5} | {row['English Name']}")

print("-" * 50)

# Try matplotlib visualization
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    plt.figure(figsize=(10, 8))
    plt.scatter(df_indic['Date'], df_indic['English Name'], color='teal', s=100)
    plt.hlines(y=df_indic['English Name'], xmin=df_indic['Date'].min(), xmax=df_indic['Date'], color='skyblue', alpha=0.5)
    plt.title('Timeline of Standardization: Indian & Brahmic Scripts (ISO 15924)', fontsize=14)
    plt.xlabel('Date of ISO Registration/Standardization', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(2))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig('kannada_script_timeline.png')
    print("\n[SUCCESS] Timeline plot saved as 'kannada_script_timeline.png'")

except ImportError:
    print("\n[INFO] 'matplotlib' not found. Skipping image generation.")
    print("You can see the text-based timeline above.")
