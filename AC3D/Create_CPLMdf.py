import pandas as pd
import os
from AC3D import PATH

def get_CPLM_data(path):
    """
    Reads the initial data from CPLM, processes it, and creates dictionaries.

    Parameters
    ----------
    path : str
        The path to the initial data file from CPLM.

    Returns
    -------
    None
    """
    
    # Read the initial data from CPLM
    filepath = path
    CPLM_initial_dataframe = pd.read_table(filepath, delimiter='\t', header=None)
    
    # Keep only the useful information
    df = CPLM_initial_dataframe.iloc[:, [0, 1, 2, 4, 5, 6]]
    df.columns = ["CPLM_id", "Accession_Number", "Position", "Gene_Name", "Species", "Sequence"]
    
    # Dictionary with CPLM ids as keys and positions as values
    CPLM_positions = {}
    positions = []
    ii = 0
    for i in df.index:
        
        if not df.duplicated(subset=["CPLM_id"])[i]:
            CPLM_positions[df["CPLM_id"][ii]] = positions
            ii = i
            positions = []
        
        positions.append(df["Position"][i])
    if positions != []:
        CPLM_positions[df["CPLM_id"][ii]] = positions   
      
    # Dictionary with Accession numbers as keys and CPLMids as values
    dff = df.drop_duplicates(subset=["CPLM_id"])
    dff = dff.drop(columns=["Position"])
    dff = dff.dropna()
    
    protein_names = {}
    CPLM_ids = []
    ii = 0
    for i in dff.index:
        
        if not dff.duplicated(subset=["Accession_Number"])[i]:
            protein_names[dff["Accession_Number"][ii]] = CPLM_ids
            ii = i
            CPLM_ids = []
        
        CPLM_ids.append(dff["CPLM_id"][i])
    if CPLM_ids != []:
        protein_names[dff["Accession_Number"][ii]] = positions  
    
    # Dictionary with Gene names as keys and CPLM ids as values
    dff2 = df.drop_duplicates(subset=["CPLM_id"])
    dff2 = dff2.drop(columns=["Position"])
    dff2 = dff2.dropna()
    
    gene_names = {}
    CPLM_ids2 = []
    iii = 0
    for i in dff2.index:
        
        if not dff.duplicated(subset=["Gene_Name"])[i]:
            gene_names[dff2["Gene_Name"][iii]] = CPLM_ids2
            iii = i
            CPLM_ids2 = []

        CPLM_ids2.append(dff2["CPLM_id"][i])
    if CPLM_ids2 != []:
        gene_names[dff2["Gene_Name"][iii]] = positions  
    
    # Save dictionaries as txt files
    with open(os.path.join(PATH.PATH().data_path, 'positions.txt'), 'w') as f:
        print(CPLM_positions, file=f)
    with open(os.path.join(PATH.PATH().data_path, 'CPLMids.txt'), 'w') as f:
        print(protein_names, file=f)
    with open(os.path.join(PATH.PATH().data_path, 'genenames.txt'), 'w') as f:
        print(gene_names, file=f)

    