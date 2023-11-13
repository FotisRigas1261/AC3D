import AC3D.Querry as q
import sys
import AC3D.Lysine_acetylation_conservation as lys
import AC3D.accessibility as acc
import pandas as pd
import logging
import os
from AC3D import PATH, get_from_uniprot, file_parser, organiser

Report_name = 'Report.csv'
BLAST = False

logging.basicConfig(
    level = logging.INFO,
    format = '[%(asctime)s] %(levelname)s: %(message)s',
    datefmt = '%d/%m %H:%M:%S',
    force=True
)

def main(Querry_string):
    
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
    Acetylation_scores=[]
    if BLAST:
        lys.run_blast(Uniprot_id_of_Querry)
        Acetylation_scores=lys.conservation_score(Uniprot_id_of_Querry,Lysine_positions)
    
    
    ##4. Get gff NEEDED
    get_from_uniprot.get_uniprot_gff(Uniprot_id_of_Querry)
    #This is hard-coded based on the previous outputs
    gff_filepath=os.path.join(PATH.TEMP, 'uniprot.gff')
    file_parser.parse_gff(gff_filepath)
    
    ##5. Distance
    cif_path = file_parser.get_cif_file(Uniprot_id_of_Querry)
    d = file_parser.get_distances(file_parser.parse_cif_file(cif_path),Lysine_positions)
    for key in d.keys():
        logging.debug(int(min(d[key]) < 7))
    
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
    logging.info("AC3D Finished")
    return Report

def get_output():
    path = os.path.join(PATH.OUTPUT, Report_name)
    return pd.read_csv(path)
    

if __name__ == "__main__":
    #Find the querried string
    Querry_string = ""
    if len(sys.argv) == 1:
        logging.info("Welcome to the protein acetylation tool!\n")
        Querry_string = input('Type the name of the protein you want to investigate or a CPLM id: ')
    else:
        Querry_string = sys.argv[1]
        if len(sys.argv) == 3:
            Report_name = sys.argv[2]
    main(Querry_string)