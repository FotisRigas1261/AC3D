import pandas as pd

def get_CPLM_data(path):

    #This file creates a csv folder from the initial txt from cplm
    filepath = path
    
    #CPLM_initial_dataframe = pd.read_csv(filepath, delimiter='\t')
    CPLM_initial_dataframe = pd.read_table(filepath, delimiter='\t', header=None)
    
    #Only keep the useful information of the initial array
    df=CPLM_initial_dataframe.iloc[:,[0,1,2,4,5,6]]
    df.columns = ["CPLM_id", "Accession_Number", "Position", "Gene_Name","Species","Sequence"]
    
    ##DICTIONARY with CPLM ids as keys and positions as values
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
      
        
    ##DICTIONARY with Accession numbers as keys and CPLMids as values
    #create a dict with all CPLM_ids for each unique protein name
    dff = df.drop_duplicates(subset=["CPLM_id"])
    dff = dff.drop(columns=["Position"])
    dff = dff.dropna()
    
    duplicated_proteins=dff.duplicated(subset=["Accession_Number"])
    protein_names = {}
    CPLM_ids = []
    ii = 0
    for i in dff.index:
        
        if duplicated_proteins[i]==False:
            protein_names[dff["Accession_Number"][ii]] = CPLM_ids
            ii = i
            CPLM_ids = []
        
        CPLM_ids.append(dff["CPLM_id"][i])
    if CPLM_ids != []:
        protein_names[dff["Accession_Number"][ii]] = positions  
    
    ##DICTIONARY with Gene names as keys and CPLM ids as values
    dff2 = df.drop_duplicates(subset=["CPLM_id"])
    dff2 = dff2.drop(columns=["Position"])
    dff2 = dff2.dropna()
    
    duplicated_names=dff.duplicated(subset=["Gene_Name"])
    gene_names = {}
    CPLM_ids2 = []
    iii = 0
    for i in dff2.index:
        
        if duplicated_names[i]==False:
            gene_names[dff2["Gene_Name"][iii]] = CPLM_ids2
            iii = i
            CPLM_ids2 = []

        CPLM_ids2.append(dff2["CPLM_id"][i])
    if CPLM_ids2 != []:
        gene_names[dff2["Gene_Name"][iii]] = positions  
    

    # save dicts as txt files
    with open('positions.txt', 'w') as f:
        print(CPLM_positions, file=f)
    with open('CPLMids.txt', 'w') as f:
        print(protein_names, file=f)
    with open('genenames.txt', 'w') as f:
        print(gene_names, file=f)

    #df.to_csv('data.csv', index=False)
