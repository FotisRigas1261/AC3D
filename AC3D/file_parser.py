import os
import pandas as pd
import re
import math
import logging
from AC3D import PATH

def parse_gff(UniprotGff):
    #Keyword will be needed to split the gff files into mutations and structures
    mut_keyword1="Mutagenesis"
    mut_keyword2="Natural variant"
    mutations_data = []
    structure_data = []
    natural_variants=[]
    filtered_Structure = pd.DataFrame()
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
                        
                        mtype,effect,source = None,None,None
                        
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
                        source=None
                        if match3:
                            source = "PubMed:"+match3.group(1)

                        mutations_data.append([position,mtype,effect,source])
                        if len(mutations_data)>0:
                            mutations_df = pd.DataFrame(mutations_data, columns=["Position","Type of mutation","Effect","Evidence"])

                    #####################################
                    #Creating Natural variant dataframe
                    #####################################
                    if mut_keyword2 in line:
                        
                        mtype,effect,source = None,None,None
                        
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
                            if match2b != None:
                                effect = match2b.group(1)
                            else:
                                effect = ""
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
                    if not (mut_keyword1 in line or mut_keyword2 in line) and not line.startswith("#") and line:
                        #This makes sure that all lines of the gff not refering to muatuions and natural variants are kept
                        columns = line.strip().split('\t')
                        if len(columns) < 4:
                            break
                        start_position=columns[3]
                        end_position=columns[4]
                        structure=columns[2]
                        structure_data.append([start_position,end_position,structure])
                        #But, many lines of the file contain info about disulfide bonds and PTM data (of AA which are not K),
                        #as well as information about secondary structure which we already get in a more complete manner,
                        #and are thus irrelevant. Here we decide to only keep data about signal peptides, binding sites and 
                        #active sites    
                        if len(structure_data)>0:
                            structures_df=pd.DataFrame(structure_data, columns=["Start position","End position","Structure"])
                            mask = (structures_df['Structure'] == 'Active site') | (structures_df['Structure'] == 'Signal peptide') | (structures_df['Structure'] == 'Binding site')
                            filtered_Structure=structures_df[mask].copy()
    except FileNotFoundError:
            logging.error(f"File not found: {UniprotGff}")

    if not filtered_Structure.empty:
        structurepath = os.path.join(PATH.PATH().temp_path, 'structures.csv')
        filtered_Structure.to_csv(structurepath, index=False)
    if len(mutations_data)>0:
        mutationspath = os.path.join(PATH.PATH().temp_path, 'mutations.csv')
        mutations_df.to_csv(mutationspath, index=False)
    if len(natural_variants)>0:
        nvariantspath = os.path.join(PATH.PATH().temp_path, 'natural_variants.csv')
        natural_variants_df.to_csv(nvariantspath, index=False)

def parse_accessibility_csv(Accessibility_file):
    Access_data_Frame = pd.read_csv(Accessibility_file)
    columns_to_keep = ['AA', 'position', 'structure_group','IDR','high_acc_5','low_acc_5']
    data_to_keep = Access_data_Frame[columns_to_keep]
    return data_to_keep

def parse_mutations_csv(mutations_file):
    mutations_data_frame = pd.read_csv(mutations_file)
    return mutations_data_frame

def parse_natural_variants_csv(variants_file):
    natural_variants_data_frame = pd.read_csv(variants_file)
    return natural_variants_data_frame

def parse_structures_csv(structures_file):
    structures_data_frame = pd.read_csv(structures_file)
    return structures_data_frame

#a link for the .cif file must be given
#This function returns a table containing the mean positions of all amino-acids
def parse_cif_file(link_to_cif):
    column9 = []
    column11 = []
    column12 = []
    column13 = []
    with open(link_to_cif, 'r') as input_file:
        for line in input_file:
            if line.startswith('ATOM'):
                # Split the line by whitespace
                elements = line.split()

                # Check if the line has enough elements
                if len(elements) >= 13:
                    column9.append(elements[8])
                    column11.append(elements[10])
                    column12.append(elements[11])
                    column13.append(elements[12])
    # Create a DataFrame from the extracted elements
    data = {
        'AA': column9,
        'x_coor': column11,
        'y_coor': column12,
        'z_coor': column13
    }
    Atoms = pd.DataFrame(data)
    #Atoms['AA'] = pd.to_numeric(Atoms['AA'], errors='coerce')
    Atoms['x_coor'] = pd.to_numeric(Atoms['x_coor'], errors='coerce')
    Atoms['y_coor'] = pd.to_numeric(Atoms['y_coor'], errors='coerce')
    Atoms['z_coor'] = pd.to_numeric(Atoms['z_coor'], errors='coerce')
    AA_mean_positions = Atoms.groupby('AA').mean().reset_index()
    #logging.debug(AA_mean_positions)
    return AA_mean_positions



#This function should use the dataframe: AA_mean_positions and the list: acetylated lysine positions to give the distance of an
#acetylated lysine from the protein binding and active sites as well as signal peptides, if they exist
#In the dictionary that is returned, the key is the lysine and the values is the list with the distances of the acet.lysines
#from the before mentioned structures. All structures are saved in the same list, but the order of the structures in the primary 
#structure is respected inside the list. For example, if [1,2,3] the list and there is a signal peptide, b.site1, b.site2
#distance 1 refers to signal peptide, 2 to b.site1, 3 to b.site2
def get_distances(AA_mean_positions,acetylated_lysines_positions):
    Distances_dictionary={} #Initiate the dictionary that will be returned in the end
    #First create a table with the coordinates of the acetylated lysines: acet_lysines_mean_positions
    AA_mean_positions['AA'] = pd.to_numeric(AA_mean_positions['AA'], errors='coerce')
    acet_lysines_mean_positions=AA_mean_positions[AA_mean_positions['AA'].isin(acetylated_lysines_positions)]

    #Then check for the existance of a structure.csv file. This type of file only exists if in the gff file
    # there is available info about binding sites, active sites or signal peptides    
    structure_filepath = os.path.join(PATH.PATH().temp_path, 'structures.csv')
    if os.path.exists(structure_filepath):
        structures_df=parse_structures_csv(structure_filepath)
        #What we need now is to create a list of aminoacids that take part into each binding site and a list of active site amino-acids
        #This can be stored in a dictionary
        site_positions = {}
        for index, row in structures_df.iterrows():
            start = row['Start position']
            end = row['End position']
            structure = row['Structure']

            # If the structure is not in the dictionary, add it with an initial entry
            if structure not in site_positions:
                site_positions[structure] = []
                site_positions_counter = 1

            # Generate a range of positions and append to the appropriate list with numerical suffix
            binding_positions = list(range(start, end + 1))
            
            # Create the key if it doesn't exist and then extend it
            key = f"{structure}{site_positions_counter}"
            if key not in site_positions:
                site_positions[key] = []
            site_positions[key].extend(binding_positions)

            # Increment the numerical suffix
            site_positions_counter += 1
        #The previous process creates a dictionary that contains some empty items. Delete empty items:
        filtered_site_positions = {key: value for key, value in site_positions.items() if any(char.isdigit() for char in key)}
    #if the structure file does not exist
     
        #Now, in order to create a dictionary with all the distances, first iterate through the lysines
        for lysine in acet_lysines_mean_positions.itertuples():
            Distances_from_all_structures=[] #This is the final list we want to fill for each lysine
            #Now iterate through the structure dictionary items. If their values list is equal to 1, directly get the distance from lys
            for binding_site,Amino_acids in filtered_site_positions.items():
                #Τhis creates a dataframe out of each one of the binding sites or structures in general
                #Inside these dataframes there is the coordinates, that will be used to calculate the distance
                binding_site=pd.DataFrame()
                binding_site=AA_mean_positions[AA_mean_positions['AA'].isin(Amino_acids)]

                #Now, for each of the acetylated lysines, calculate the distance from each binding site AA and store in list
                binding_site_AA_distances_from_Lysine=[]
                for AA in binding_site.itertuples():                   
                    #Euclidian distance
                    Distance = math.sqrt((AA.x_coor - lysine.x_coor)**2 + (AA.y_coor - lysine.y_coor)**2 + 
                                        (AA.z_coor - lysine.z_coor)**2)
                    binding_site_AA_distances_from_Lysine.append(Distance)
                    #Now only the smallest distnance in the list must be kept, and this will be the final distance from the bind.site
                distance_from_structure=None
                if binding_site_AA_distances_from_Lysine:
                    distance_from_structure=min(binding_site_AA_distances_from_Lysine)
                #Now fill the list with all the distances
                #In this list there is the proximity of a lysine to each structure, the first structure in the primary 
                #sequence has the first distance in the list etc
                if distance_from_structure:
                    Distances_from_all_structures.append(distance_from_structure)
                #Round to 2 decimals to make the file readable
            for i in range(len(Distances_from_all_structures)):
                Distances_from_all_structures[i] = round(Distances_from_all_structures[i], 2)

            #Fill the initial dictionary        
            Distances_dictionary[lysine.AA] = Distances_from_all_structures
    else:
        #If there is no structural information, return an empty dictionary
        Distances_dictionary={}
    
    logging.debug(Distances_dictionary)
    return Distances_dictionary
            

    
def get_cif_file(name=None):
    cif_directory = os.path.join(PATH.PATH().temp_path, "acetylation_cif")
    cif_files = os.listdir(cif_directory)
    if name !=None:
        cif_file_name = name+".cif"
        if cif_file_name in cif_files:
            link_to_cif = os.path.join(cif_directory, cif_file_name)   
            return link_to_cif
    elif cif_files[0].endswith(".cif"):
        link_to_cif = os.path.join(cif_directory, cif_files[0])   
        return link_to_cif





