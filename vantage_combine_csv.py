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
    if "_RUO" in csv:
        csv_ruo = csv
    elif "sample_results" in csv:
        csv_qual = csv
    else:
        pass
    
df_qual = pd.read_csv(csv_qual, header=11)
df_ruo = pd.read_csv(csv_ruo)

print("RUO File: ", csv_ruo)
print("Qual File: ", csv_qual)

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

df_new = df_ruo
df_new['Interpretive Result'] = None
df_new['Action*'] = None
df_new = df_new.drop(df_new.columns[[5, 10, 11, 12, 13, 14]], axis=1)
well_list = list(set(df_new['Well'].to_list()))

for w in well_list:
    index_list = df_qual.index[df_qual['Well'] == w]
    index = int(index_list[0])
    sample = df_qual.iloc[index, 2]
    inter_result = df_qual.iloc[index, 6]
    action = df_qual.iloc[index, 7]
    new_row = {'Well':w, 'Sample':sample, 'Target':'A_Qual', 'Interpretive Result':inter_result, 'Action*':action}
    df_new = df_new.append(new_row, ignore_index=True)

df_new = df_new.sort_values(by = ['Well', 'Target'])

df_new.to_csv(output_file_name, index=False)