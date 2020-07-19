import pandas as pd
from tkinter.filedialog import askopenfilename
import tkinter as tk

def csv_combine():
	print("Select the Qualitative CSV File")
	proceed = input("Hit Enter to Continue")
	tk.Tk().withdraw()
	csv_qual = askopenfilename()
	print(csv_qual)

	print("Select the RUO CSV File")
	proceed = input("Hit Enter to Continue")
	csv_ruo = askopenfilename()
	print(csv_ruo)

	run_name = input("Enter a name for the run (no spaces or / ): ")
	output_file_name = run_name + '_combined_file.csv'
	  
	df_qual = pd.read_csv(csv_qual, skiprows=12)
	df_qual.to_csv('testqual.csv', index=False)
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

csv_combine()
start_again = 'yes'
while start_again == 'yes':
	start_again = input("Do you want to run the program again? (Type 'yes' to continue):  ")
	if start_again == 'yes':
		csv_combine()
	else:
		start_again = 'no'