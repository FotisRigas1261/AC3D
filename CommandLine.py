import pandas as pd

print("Welcome to the protein acetylation website!\n")

#############################################################
### Create the Acetylation Database from the CPLM txt file###
#############################################################

filepath = '3rd Semester/Project/Acetylation.txt'
#CPLM_initial_dataframe = pd.read_csv(filepath, delimiter='\t')
CPLM_initial_dataframe = pd.read_table(filepath, delimiter='\t', header=None)

#Only keep the useful information of the initial array
final_CPLM_dataframe=CPLM_initial_dataframe.iloc[:,[0,1,2,4,5,6]]
#print(final_CPLM_dataframe.iloc[200,0])
#print(final_CPLM_dataframe.iloc[:,[0,1,2,3,4]]) #column 5 is the sequence
final_CPLM_dataframe.columns = ["CPLM_id", "Accession_Number", "Position", "Protein_Name","Species","Sequence"]

############
###Querry###
############

Querry = input('Type the name of the protein you want to investigate: ')

#find if the querry existsin any of the possible columns
resultCPLMid = final_CPLM_dataframe['CPLM_id'].str.contains(Querry)
countCPLMid = resultCPLMid.sum()
resultAccession_Number = final_CPLM_dataframe['Accession_Number'].str.contains(Querry)
countAccession_Number = resultAccession_Number.sum()
resultProtein_Name = final_CPLM_dataframe['Protein_Name'].str.contains(Querry)
countProtein_Name = resultProtein_Name.sum()

if not resultCPLMid.any() and not resultAccession_Number.any() and not resultProtein_Name.any():
    print("No match for the querry!")
else:
    #Set querry index to -1 so it doesnt match anywhere
    querry_index=-1

    #I did all this so that someone can search in either way - Accession number, CPLM number or protein name
    #for some reason protein name based querry does not work
    if countCPLMid == 0 and countAccession_Number == 0:
        querry_index = resultProtein_Name.idxmax()
    elif countCPLMid == 0 and countProtein_Name == 0:
        querry_index = resultAccession_Number.idxmax()
    elif countAccession_Number == 0 and countProtein_Name == 0:
        querry_index = resultCPLMid.idxmax()
    else:
        print("Error: There should not be a protein with overlaping name, CPLMid or accession number!")

    #Name: 2, dtype: object - this comes after printing, has to be removed
    print(final_CPLM_dataframe.iloc[querry_index,[0,1,3,4]])
    print(final_CPLM_dataframe.iloc[querry_index,[5]])

    query_cplmid = final_CPLM_dataframe.loc[querry_index, 'CPLM_id']
    # Create a list of tuples with the same CPLMid as the query
    matching_tuples = final_CPLM_dataframe[final_CPLM_dataframe['CPLM_id'] == query_cplmid].itertuples(index=False, name=None)

    print("Positions of Lysine acetylations:")
    for tup in matching_tuples:
        third_element = tup[2]  # 3rd element (index 2)
        print(third_element)
