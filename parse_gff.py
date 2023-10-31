import os
import pandas as pd
import re

def parse_gff(UniprotGff):
    #Keyword will be needed to split the gff files into mutations and structures
    mut_keyword="Mutagenesis"
    mutations_data = []
    structure_data = []
    try:
        with open(UniprotGff, "r") as file:
            for line in file:
                #####################################
                #First, creating mutations data frame
                #####################################
                if mut_keyword in line:
                    #getting the positions
                    columns = line.strip().split('\t')
                    position = columns[3]
                    #getting mutation type
                    match1 = re.search(r'([A-Z])->([A-Z])', line)
                    if match1:
                        before = match1.group(1)
                        after = match1.group(2)
                        mtype = before + "->" + after
                    #getting the effect
                    match2 = re.search(r'Note=([^.%]+)[.%]', line)
                    effect = match2.group(1)
                    #getting the source
                    match3 = re.search(r'PubMed:([^;]+)[;]', line)
                    source = "PubMed:"+match3.group(1)

                    mutations_data.append([position,mtype,effect,source])
                    if len(mutations_data)>0:
                        mutations_df = pd.DataFrame(mutations_data, columns=["Position","Type of mutation","Effect","Evidence"])                   
                #######################################
                #Second, creating structures data frame
                #######################################
                if not mut_keyword in line and not line.startswith("#"):
                    columns = line.strip().split('\t')
                    start_position=columns[3]
                    end_position=columns[4]
                    structure=columns[2]
                    structure_data.append([start_position,end_position,structure])
                    structures_df=pd.DataFrame(structure_data, columns=["Start position","End position","Structure"])
    except FileNotFoundError:
            print(f"File not found: {UniprotGff}")

    structurepath = 'structures.csv'
    structures_df.to_csv(structurepath, index=False)
    if len(mutations_data)>0:
        mutationspath = 'mutations.csv'
        mutations_df.to_csv(mutationspath, index=False)

# UniprotGff='uniprot.gff'
# parse_gff(UniprotGff)