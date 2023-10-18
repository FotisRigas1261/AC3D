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
    
    
    #create a dict with all positions for each unique CPLM_id
    duplicated_ids=df.duplicated(subset=["CPLM_id"])
    CPLM_positions = {}
    positions = []
    ii = 0
    for i in df.index:
        
        if duplicated_ids[i]==False:
            CPLM_positions[df["CPLM_id"][ii]] = positions
            ii = i
            positions = []
        
        positions.append(df["Position"][i])
    if positions != []:
        CPLM_positions[df["CPLM_id"][ii]] = positions   
      
        
    
    #create a dict with all CPLM_ids for each unique protein name
    dff = df.drop_duplicates(subset=["CPLM_id"])
    dff = dff.drop(columns=["Position"])
    dff = dff.dropna()
    
    duplicated_proteins=dff.duplicated(subset=["Protein_Name"])
    protein_names = {}
    CPLM_ids = []
    ii = 0
    for i in dff.index:
        
        if duplicated_proteins[i]==False:
            protein_names[dff["Protein_Name"][ii]] = CPLM_ids
            ii = i
            CPLM_ids = []
        
        CPLM_ids.append(dff["CPLM_id"][i])
    if CPLM_ids != []:
        protein_names[dff["Protein_Name"][ii]] = positions  
    
    
    # save dicts as txt files
    with open('positions.txt', 'w') as f:
        print(CPLM_positions, file=f)
    with open('CPLMids.txt', 'w') as f:
        print(protein_names, file=f)
    

    #df.to_csv('data.csv', index=False)
