import pandas as pd

# load TSV file
df = pd.read_csv("df_iso15924_scripts.tsv", sep="\t")

# see first 5 rows
print(df.head())

# see column names
print(df.columns)

# number of rows
print(len(df))
