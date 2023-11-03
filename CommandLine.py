import Querry as q
import Create_CPLMdf as c
import sys
import get_from_uniprot
import Lysine_acetylation_conservation as lys
import accessibility as acc
import file_parser 
import pandas as pd
import organiser
import os

#Find the querried string
Querry_string = ""
if len(sys.argv) == 1:
    print("Welcome to the protein acetylation website!\n")
    Querry_string = input('Type the name of the protein you want to investigate or a CPLM id: ')
else:
    Querry_string = sys.argv[1]
    
#if data files do not exist yet, create them
try:
    open("../CPLMids.txt","r")
    open("../positions.txt","r")
    open("../genenames.txt","r")
except:
    c.get_CPLM_data('../Acetylation.txt')

#Set the Uniprot id
Uniprot_id_of_Querry,Lysine_positions=q.Querry(Querry_string)

#######################
##PART 1: RETRIEVE DATA
#######################

##1.Fasta sequence NOT NEEDED
get_from_uniprot.get_uniprot_fasta(Uniprot_id_of_Querry)

##2. Secondary structure NEEDED
acc.get_residue_accesibility(Uniprot_id_of_Querry)

##3.Conservation-works but slowly NEEDED
lys.run_blast(Uniprot_id_of_Querry)
Acetylation_scores=lys.conservation_score(Uniprot_id_of_Querry,Lysine_positions)

##4. Get gff NEEDED
get_from_uniprot.get_uniprot_gff(Uniprot_id_of_Querry)
#This is hard-coded based on the previous outputs
gff_filepath='uniprot.gff'
file_parser.parse_gff(gff_filepath)

###########################
##PART 2: Organise the data
###########################

#1.Parse the gff file. This is hard-coded based on the previous outputs
Accecibility_file = 'SecondaryStrAndAccessibility.csv'
Acc_dataframe=file_parser.parse_accessibility_csv(Accecibility_file)

#2.Create a DataFrame with the positions and their acetylation scores
combined_data = list(zip(Lysine_positions, Acetylation_scores))
acetylated_lysines = pd.DataFrame(combined_data, columns=['Acetylated Lysines', 'Conservation score'])

#3.Create the final report and clear the working directory
Report=organiser.combine_all_data(Acc_dataframe,acetylated_lysines)#,structures_dataframe,mutations_dataframe,natural_variants_dataframe)
organiser.clear_files()
path = 'Report.csv'
Report.to_csv(path, index=False)

