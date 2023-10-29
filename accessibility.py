# -*- coding: utf-8 -*-



import numpy as np
import structuremap.utils
structuremap.utils.set_logger()
from structuremap.processing import download_alphafold_cif, download_alphafold_pae, format_alphafold_data, annotate_accessibility, get_smooth_score, annotate_proteins_with_idr_pattern, get_extended_flexible_pattern, get_proximity_pvals, perform_enrichment_analysis, perform_enrichment_analysis_per_protein, evaluate_ptm_colocalization, extract_motifs_in_proteome
import os



output_dir = r"D:\文件\doc_2024\integrated project\program"

cif_dir = os.path.join(output_dir, 'acetylation_cif')
pae_dir = os.path.join(output_dir, 'acetylation_pae')


def get_residue_accesibility(uniprot_ID):
    
    
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
    
    
    alphafold_accessibility_smooth = get_smooth_score(
    alphafold_accessibility, 
    np.array(['nAA_24_180_pae']), 
    [10])
    
    alphafold_accessibility_smooth['IDR'] = np.where(
    alphafold_accessibility_smooth['nAA_24_180_pae_smooth10']<=34.27, 1, 0)
    
    return alphafold_accessibility_smooth



access = get_residue_accesibility(['O00115'])


print(access)   
    
    
    
    
    
    







