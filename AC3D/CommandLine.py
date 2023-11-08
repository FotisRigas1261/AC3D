import Querry as q
import Create_CPLMdf as c
import sys
import get_from_uniprot
import Lysine_acetylation_conservation as lys
import accessibility as acc
import file_parser 
import pandas as pd
import organiser
import logging
import os
import PATH

def main():
    
    logging.basicConfig(
        level = logging.DEBUG, #level = logging.INFO,
        format = '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt = '%d/%m %H:%M:%S',
        force=True
    )
    
    #Find the querried string
    Querry_string = ""
    Report_name = 'Report.csv'
    if len(sys.argv) == 1:
        logging.info("Welcome to the protein acetylation tool!\n")
        Querry_string = input('Type the name of the protein you want to investigate or a CPLM id: ')
    else:
        Querry_string = sys.argv[1]
        if len(sys.argv) == 3:
            Report_name = sys.argv[2]
        
    #if data files do not exist yet, create them
    try:
        open(os.path.join(PATH.DATA, "CPLMids.txt"),"r")
        open(os.path.join(PATH.DATA, "positions.txt"),"r")
        open(os.path.join(PATH.DATA, "genenames.txt"),"r")
    except:
        c.get_CPLM_data(os.path.join(PATH.DATA, 'Acetylation.txt'))
    
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
    gff_filepath=os.path.join(PATH.TEMP, 'uniprot.gff')
    file_parser.parse_gff(gff_filepath)
    
    ###########################
    ##PART 2: Organise the data
    ###########################
    
    #1.Parse the gff file. This is hard-coded based on the previous outputs
    Accecibility_file = os.path.join(PATH.TEMP, 'SecondaryStrAndAccessibility.csv')
    Acc_dataframe=file_parser.parse_accessibility_csv(Accecibility_file)
    
    #2.Create a DataFrame with the positions and their acetylation scores
    combined_data = list(zip(Lysine_positions, Acetylation_scores))
    acetylated_lysines = pd.DataFrame(combined_data, columns=['Acetylated Lysines', 'Conservation score'])
    
    #3.Create the final report and clear the working directory
    Report=organiser.combine_all_data(Acc_dataframe,acetylated_lysines)
    organiser.clear_files()
    organiser.ensure_uniform_format(Report)
    path = os.path.join(PATH.OUTPUT, Report_name)
    Report.to_csv(path, index=False)

if __name__ == "__main__":
    main()