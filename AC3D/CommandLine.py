import AC3D.Querry as q
import sys
import AC3D.Lysine_acetylation_conservation as lys
import AC3D.accessibility as acc
import pandas as pd
import logging
import os
from AC3D import PATH, get_from_uniprot, file_parser, organiser

Report_name = 'Report.csv'

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%d/%m %H:%M:%S',
    force=True
)

def main(Querry_string, BLAST=True, report_path=None):
    """
    Fetches data concerning acetylated lysines, processes the data, and combines it into a dataframe.

    Parameters
    ----------
    Querry_string : str
        The id of a protein, which can be a Uniprot id, CPLM id, or a gene name.
    BLAST : bool, optional
        Turn on or off the calculation of conservation scores, which uses blast (default is True).
    report_path : str, optional
        The path where the report should be saved. If None, it uses the default path.

    Returns
    -------
    report : pandas.DataFrame
        A dataframe that combines all data collected and processed.
    """
    
    # Set the Uniprot id
    Uniprot_id_of_Querry, Lysine_positions = q.Querry(Querry_string)
    PATH.PATH(Uniprot_id_of_Querry)
    
    # Part 1: Retrieve Data
    
    # 1. Fasta sequence (NOT NEEDED)
    get_from_uniprot.get_uniprot_fasta(Uniprot_id_of_Querry)
    
    # 2. Secondary structure (NEEDED)
    acc.get_residue_accesibility(Uniprot_id_of_Querry)
    
    # 3. Conservation (NEEDED)
    Acetylation_scores = [None] * len(Lysine_positions)
    if BLAST:
        lys.run_blast(Uniprot_id_of_Querry)
        Acetylation_scores = lys.conservation_score(Uniprot_id_of_Querry, Lysine_positions)
    
    # 4. Get gff (NEEDED)
    get_from_uniprot.get_uniprot_gff(Uniprot_id_of_Querry)
    gff_filepath = os.path.join(PATH.PATH().temp_path, 'uniprot.gff')
    file_parser.parse_gff(gff_filepath)
    
    # 5. Distance
    cif_path = file_parser.get_cif_file(Uniprot_id_of_Querry)
    distances_dict = file_parser.get_distances(file_parser.parse_cif_file(cif_path), Lysine_positions)

    # Part 2: Organise the Data
    
    # 1. Parse the gff file
    Accessibility_file = os.path.join(PATH.PATH().temp_path, 'SecondaryStrAndAccessibility.csv')
    Acc_dataframe = file_parser.parse_accessibility_csv(Accessibility_file)
    
    # 2. Combine the accessibility dataframe and dictionary with distances into one dataframe
    dataframe = organiser.combine_df_dict(Acc_dataframe, distances_dict)
    
    # 3. Create a DataFrame with the positions and their acetylation scores
    combined_data = list(zip(Lysine_positions, Acetylation_scores))
    acetylated_lysines = pd.DataFrame(combined_data, columns=['Acetylated Lysines', 'Conservation score'])
    
    # 4. Create the final report and clear the working directory
    report = organiser.combine_all_data(dataframe, acetylated_lysines)
    
    # If a custom report path is provided, save the report there; otherwise, use the default path
    if report_path is not None:
        path = os.path.join(report_path, Report_name)
    else:
        path = os.path.join(PATH.PATH().output_path, Report_name)
    
    report.to_csv(path, index=False)
    logging.info("AC3D Finished")
    return report

def get_output(report_path=None):
    """
    Gets the output report from the specified path.

    Parameters
    ----------
    report_path : str, optional
        The path where the report is saved. If None, it uses the default path.

    Returns
    -------
    report : pandas.DataFrame
        The dataframe containing the acetylation data.
    """
    if report_path is not None:
        path = os.path.join(report_path, Report_name)
    else:
        path = os.path.join(PATH.PATH().output_path, Report_name)
    return pd.read_csv(path)

if __name__ == "__main__":
    # Find the queried string
    Querry_string = ""
    report_path = None
    
    if len(sys.argv) == 1:
        logging.info("Welcome to the protein acetylation tool!\n")
        Querry_string = input('Type the name of the protein you want to investigate or a CPLM id: ')
    else:
        Querry_string = sys.argv[1]
        if len(sys.argv) >= 3:
            BLAST = eval(sys.argv[2])
            if len(sys.argv) >= 4:
                report_path = sys.argv[3]
    
    main(Querry_string, BLAST, report_path)

