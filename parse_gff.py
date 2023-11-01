import os
import pandas as pd
import re

def parse_gff(UniprotGff):
    #Keyword will be needed to split the gff files into mutations and structures
    mut_keyword1="Mutagenesis"
    mut_keyword2="Natural variant"
    mutations_data = []
    structure_data = []
    natural_variants=[]
    try:
        with open(UniprotGff, "r") as file:
            line_count = 0

            for line in file:
                line_count += 1
            if line_count > 2:
                #return to the begining of the file
                file.seek(0)
                for line in file:
                #####################################
                #First, creating mutations data frame
                #####################################
                #If the keyword is mutagenesis
                    if mut_keyword1 in line:
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

                    #####################################
                    #Creating Natural variant dataframe
                    #####################################
                    if mut_keyword2 in line:
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
                        match2 = re.search(r'dbSNP:([^.,]+)[.,]?', line)
                        if match2:
                            effect = match2.group(1)
                        else:
                            match2b = re.search(r'AIPCS%([^%.]+)[%.]', line)
                            effect = match2b.group(1)
                        #getting the source
                        match3 = re.search(r'PubMed:([^;,]+)[;,]', line)
                        if match3:
                            source = "PubMed:"+match3.group(1)
                        else:
                            source=" "
                        natural_variants.append([position,mtype,effect,source])
                        if len(natural_variants)>0:
                            natural_variants_df = pd.DataFrame(natural_variants, columns=["Position","Type of variation","Effect","Evidence"])              
                    #######################################
                    #Second, creating structures data frame
                    #######################################
                    if not (mut_keyword1 in line or mut_keyword2 in line) and not line.startswith("#"):
                        columns = line.strip().split('\t')
                        start_position=columns[3]
                        end_position=columns[4]
                        structure=columns[2]
                        structure_data.append([start_position,end_position,structure])
                        if len(structure_data)>0:
                            structures_df=pd.DataFrame(structure_data, columns=["Start position","End position","Structure"])
    except FileNotFoundError:
            print(f"File not found: {UniprotGff}")

    if len(structure_data)>0:
        structurepath = 'structures.csv'
        structures_df.to_csv(structurepath, index=False)
    if len(mutations_data)>0:
        mutationspath = 'mutations.csv'
        mutations_df.to_csv(mutationspath, index=False)
    if len(natural_variants)>0:
        nvariantspath = 'natural_variants.csv'
        natural_variants_df.to_csv(nvariantspath, index=False)

# UniprotGff='uniprot.gff'
# parse_gff(UniprotGff)