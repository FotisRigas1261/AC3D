import Querry as q
import Create_CPLMdf as c
import sys
import get_from_uniprot
import alphafold
import Lysine_acetylation_conservation as lys



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
except:
    c.get_CPLM_data('../Acetylation.txt')

#Set the Uniprot id
Uniprot_id_of_Querry,Lysine_positions=q.Querry(Querry_string)

######
##TEST: use the uniprot id to get information
######

#1.Fasta sequence
get_from_uniprot.get_uniprot_fasta(Uniprot_id_of_Querry)
get_from_uniprot.print_data(Uniprot_id_of_Querry)

#2.PDB files from alphafold
link = alphafold.get_alphafold_download_link(Uniprot_id_of_Querry)
#print(link)
#alphafold.parse_pdb(link)

##3.Conservation
#lys.run_blast(Uniprot_id_of_Querry)
#print(lys.conservation_score(Uniprot_id_of_Querry,Lysine_positions))

