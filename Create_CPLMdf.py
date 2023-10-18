import pandas as pd

#############################################################
### Create the Acetylation Database from the CPLM txt file###
#############################################################

def get_CPLM_data(path):

    #This file creates a csv folder from the initial txt from cplm
    filepath = path
    
    #CPLM_initial_dataframe = pd.read_csv(filepath, delimiter='\t')
    CPLM_initial_dataframe = pd.read_table(filepath, delimiter='\t', header=None)
    
    #Only keep the useful information of the initial array
    df=CPLM_initial_dataframe.iloc[:,[0,1,2,4,5,6]]
    #print(final_CPLM_dataframe.iloc[200,0])
    #print(final_CPLM_dataframe.iloc[:,[0,1,2,3,4]]) #column 5 is the sequence
    df.columns = ["CPLM_id", "Accession_Number", "Position", "Protein_Name","Species","Sequence"]
    
    duplicated_first=df.duplicated(subset=["CPLM_id"])
    CPLM_positions = {}
    positions = []
    ii = 0
    for i in df.index:
        
        if duplicated_first[i]==False:
            CPLM_positions[df["CPLM_id"][ii]] = positions
            ii = i
            positions = []
        
        positions.append(df["Position"][i])
    CPLM_positions[df["CPLM_id"][ii]] = positions   
      
        
    #print(CPLM_positions)
    
    dff = df.drop_duplicates(subset=["CPLM_id"])
    dff = dff.drop(columns=["Position"])
    
    dff.to_csv('data.csv', index=False)
    
    return CPLM_positions