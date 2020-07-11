import pandas as pd
import os

start = input("Are both .csv files present? Type 'yes' and hit Enter.  ")
if start != 'yes':
	exit()
else:
	pass

run_name = input("Enter a name for the run (no spaces or / ): ")
output_file_name = run_name + '_combined_file.csv'

csvs = []
files = os.listdir()
for file in files:
    if file[-3:] == "csv":
        csvs.append(file)
    else:
        pass
for csv in csvs:
    if "RUO" in csv:
        csv_ruo = csv
    elif "Qual" in csv:
        csv_qual = csv
    else:
        pass
    
df_qual = pd.read_csv(csv_qual, header=12)
df_ruo = pd.read_csv(csv_ruo)

def well_standard(x):
    if len(x) < 3:
        alpha = x[:1]
        numb = x[1:]
        numb = '0' + numb
        x = alpha + numb
        return(x)
    else:
        return(x)

df_ruo['Well'] = df_ruo['Well'].apply(well_standard)
df_join = pd.merge(df_ruo, df_qual, on='Well', how='right')
df_join.to_csv(output_file_name)