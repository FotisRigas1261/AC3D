import Querry as q
import Create_CPLMdf as c
import sys
import get_from_uniprot
import alphafold
import Lysine_acetylation_conservation as lys
import accessibility as acc


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

##1.Fasta sequence
get_from_uniprot.get_uniprot_fasta(Uniprot_id_of_Querry)
get_from_uniprot.print_data(Uniprot_id_of_Querry)

##2. Secondary structure
acc.get_residue_accesibility(Uniprot_id_of_Querry)

##3.Conservation-works but slowly
#lys.run_blast(Uniprot_id_of_Querry)
print(lys.conservation_score(Uniprot_id_of_Querry,Lysine_positions))

##4. Get gff
#print(get_from_uniprot.get_uniprot_gff(Uniprot_id_of_Querry))
#WORKS print(get_from_uniprot.function_site(Uniprot_id_of_Querry)) #This has to be parsed to create a dataframe
#get pdb files:
#get_from_uniprot.get_uniprot_pdb(Uniprot_id_of_Querry)



