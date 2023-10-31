import Querry as q
import Create_CPLMdf as c
import sys
import get_from_uniprot
import Lysine_acetylation_conservation as lys
import accessibility as acc
import parse_gff


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

######
##TEST: use the uniprot id to get information
######

##1.Fasta sequence NOT NEEDED
get_from_uniprot.get_uniprot_fasta(Uniprot_id_of_Querry)

##2. Secondary structure NEEDED
#acc.get_residue_accesibility(Uniprot_id_of_Querry)

##3.Conservation-works but slowly NEEDED
#lys.run_blast(Uniprot_id_of_Querry)
#Acetylation_scores=lys.conservation_score(Uniprot_id_of_Querry,Lysine_positions)

##4. Get gff NEEDED
get_from_uniprot.get_uniprot_gff(Uniprot_id_of_Querry)
gff_filepath='uniprot.gff'
parse_gff.parse_gff(gff_filepath)




