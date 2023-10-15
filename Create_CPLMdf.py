import pandas as pd

#############################################################
### Create the Acetylation Database from the CPLM txt file###
#############################################################

#This file creates a csv folder from the initial txt from cplm
filepath = '3rd Semester/Project/Acetylation.txt'

#CPLM_initial_dataframe = pd.read_csv(filepath, delimiter='\t')
CPLM_initial_dataframe = pd.read_table(filepath, delimiter='\t', header=None)

#Only keep the useful information of the initial array
final_CPLM_dataframe=CPLM_initial_dataframe.iloc[:,[0,1,2,4,5,6]]
#print(final_CPLM_dataframe.iloc[200,0])
#print(final_CPLM_dataframe.iloc[:,[0,1,2,3,4]]) #column 5 is the sequence
final_CPLM_dataframe.columns = ["CPLM_id", "Accession_Number", "Position", "Protein_Name","Species","Sequence"]

final_CPLM_dataframe.to_csv('data.csv', index=False)
