import numpy as np
import structuremap.utils
structuremap.utils.set_logger()
from structuremap.processing import download_alphafold_cif, download_alphafold_pae, format_alphafold_data, annotate_accessibility, get_smooth_score, annotate_proteins_with_idr_pattern, get_extended_flexible_pattern, get_proximity_pvals, perform_enrichment_analysis, perform_enrichment_analysis_per_protein, evaluate_ptm_colocalization, extract_motifs_in_proteome
import os
import PATH
import shutil
import logging






def get_residue_accesibility(id_from_uniprot):
    
    #The functions used afterwards take only lists as arguments
    uniprot_ID=[id_from_uniprot]
    
    output_dir = PATH.TEMP
    cif_dir = os.path.join(output_dir, 'acetylation_cif')
    pae_dir = os.path.join(output_dir, 'acetylation_pae')
    
    valid_proteins_cif, invalid_proteins_cif, existing_proteins_cif = download_alphafold_cif(
    proteins=uniprot_ID,
    out_folder=cif_dir)
    
    
    
    valid_proteins_pae, invalid_proteins_pae, existing_proteins_pae = download_alphafold_pae(
    proteins=uniprot_ID,
    out_folder=pae_dir, 
    )
    
    alphafold_annotation = format_alphafold_data(
    directory=cif_dir, 
    protein_ids=uniprot_ID)
    
    full_sphere_exposure = annotate_accessibility(
    df=alphafold_annotation, 
    max_dist=24, 
    max_angle=180, 
    error_dir=pae_dir)
    
    alphafold_accessibility = alphafold_annotation.merge(
    full_sphere_exposure, how='left', on=['protein_id','AA','position'])
    
    alphafold_accessibility['high_acc_5'] = np.where(alphafold_accessibility.nAA_24_180_pae <= 5, 1, 0)
    alphafold_accessibility['low_acc_5'] = np.where(alphafold_accessibility.nAA_24_180_pae > 5, 1, 0)
    
    alphafold_accessibility_smooth = get_smooth_score(
    alphafold_accessibility, 
    np.array(['nAA_24_180_pae']), 
    [10])
    
    alphafold_accessibility_smooth['IDR'] = np.where(
        #The threshold for intrinsicly disordered protein is set at 34.27, this needs further investigation
    alphafold_accessibility_smooth['nAA_24_180_pae_smooth10']<=34.27, 1, 0)
    
    #Remove excess files 
    directory_path = PATH.TEMP
    file_list = os.listdir(directory_path)
    filenames_to_Remove = ["acetylation_pae"]
    for filename in file_list:
        if any(keyword in filename for keyword in filenames_to_Remove):
            file_path = os.path.join(directory_path, filename)
            try:
                shutil.rmtree(file_path)
                logging.debug(f"Removed file: {file_path}")
            except Exception as e:
                logging.error(f"Error removing file {file_path}: {e}")

    #Store the dataframe as a csv file
    csv_file_path = os.path.join(directory_path, 'SecondaryStrAndAccessibility.csv')

    # Save the DataFrame to a CSV file
    alphafold_accessibility_smooth.to_csv(csv_file_path, index=False)

    return alphafold_accessibility_smooth

