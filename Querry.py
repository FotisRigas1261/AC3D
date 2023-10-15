def Querry(dataframe):

    Querry_string = input('Type the name of the protein you want to investigate: ')

    resultCPLMid = dataframe['CPLM_id']==Querry_string
    countCPLMid = resultCPLMid.sum()
    resultAccession_Number = dataframe['Accession_Number']==Querry_string
    countAccession_Number = resultAccession_Number.sum()
    resultProtein_Name = dataframe['Protein_Name']==Querry_string
    countProtein_Name = resultProtein_Name.sum()

    if not resultCPLMid.any() and not resultAccession_Number.any() and not resultProtein_Name.any():
        print("No match for the querry!")
    else:
        #Set querry index to -1 so it doesnt match anywhere
        querry_index=-1

        #I did all this so that someone can search in either way - Accession number, CPLM number or protein name
        #for some reason protein name based querry does not work
        if countCPLMid == 0 and countAccession_Number == 0:
            #idx.max basically takes as index the index of the first occurence of the name of the querried protein
            #This is not a problem since there is redundant information in the txt file
            querry_index = resultProtein_Name.idxmax()
        elif countCPLMid == 0 and countProtein_Name == 0:
            querry_index = resultAccession_Number.idxmax()
        elif countAccession_Number == 0 and countProtein_Name == 0:
            querry_index = resultCPLMid.idxmax()
        else:
            print("Error: There should not be a protein with overlaping name, CPLMid or accession number!")

    return dataframe.iloc[querry_index,1]
