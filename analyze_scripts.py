
import pandas as pd
import datetime

def load_dataset(filepath="df_iso15924_scripts.tsv"):
    """Loads the ISO 15924 dataset."""
    try:
        df = pd.read_csv(filepath, sep="\t")
        return df
    except FileNotFoundError:
        return None

def get_indic_scripts_list():
    """Returns a list of ISO codes for Indic/Brahmic scripts."""
    return [
        'Brah', 'Deva', 'Knda', 'Taml', 'Telu', 'Mlym', 'Beng', 'Gujr', 
        'Guru', 'Orya', 'Sinh', 'Tibt', 'Khmr', 'Java', 'Bali', 'Newa', 
        'Gran', 'Sidd'
    ]

def get_indic_script_growth(df):
    """
    Calculates the cumulative count of registered Indic scripts over time.
    Returns a DataFrame with 'Date' and 'Cumulative Count'.
    """
    indic_scripts = get_indic_scripts_list()
    df_indic = df[df['Code'].isin(indic_scripts)].copy()
    
    # Convert date, handling potential errors or formats
    df_indic['Date'] = pd.to_datetime(df_indic['Date'])
    df_indic = df_indic.sort_values('Date')
    
    # Calculate cumulative count
    df_indic['Count'] = 1
    df_indic['Cumulative Count'] = df_indic['Count'].cumsum()
    
    return df_indic[['Date', 'Code', 'English Name', 'Cumulative Count']]

def compare_kannada_latency(df):
    """
    Analyzes the time gap between the first major Indic script registration 
    and Kannada's registration.
    """
    indic_scripts = get_indic_scripts_list()
    df_indic = df[df['Code'].isin(indic_scripts)].copy()
    df_indic['Date'] = pd.to_datetime(df_indic['Date'])
    
    # Find Kannada date
    kannada_row = df_indic[df_indic['English Name'] == 'Kannada']
    if kannada_row.empty:
        return None
        
    kannada_date = kannada_row.iloc[0]['Date']
    
    # Calculate difference for all scripts relative to Kannada
    df_indic['Days Difference'] = (df_indic['Date'] - kannada_date).dt.days
    
    # Sort by date
    return df_indic.sort_values('Date')[['English Name', 'Date', 'Days Difference']]

if __name__ == "__main__":
    # Test the functions
    df = load_dataset()
    if df is not None:
        print("Dataset loaded.")
        growth = get_indic_script_growth(df)
        print("\nGrowth Tail:\n", growth.tail())
        
        latency = compare_kannada_latency(df)
        if latency is not None:
            print("\nLatency Analysis (Head):\n", latency.head())
    else:
        print("Dataset not found during test.")
