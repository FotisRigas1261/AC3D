import Querry as q
import Create_CPLMdf as c
import sys
import get_from_uniprot
import alphafold
import Lysine_acetylation_conservation as lys
import Secondary_structure_json as secnd
import pdfReportCreator

#Trial with structure map
# Import structuremap functions
import structuremap.utils
structuremap.utils.set_logger()
from structuremap.processing import download_alphafold_cif, download_alphafold_pae, format_alphafold_data, annotate_accessibility, get_smooth_score, annotate_proteins_with_idr_pattern, get_extended_flexible_pattern, get_proximity_pvals, perform_enrichment_analysis, perform_enrichment_analysis_per_protein, evaluate_ptm_colocalization, extract_motifs_in_proteome
from structuremap.plotting import plot_enrichment, plot_ptm_colocalization
import pandas as pd
import numpy as np
import os
import re
import plotly.express as px
import tqdm
import tempfile


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
FASTA = get_from_uniprot.get_uniprot_fasta(Uniprot_id_of_Querry)
#get_from_uniprot.print_data(Uniprot_id_of_Querry)

##2.PDB files from alphafold
#link = alphafold.get_alphafold_download_link(Uniprot_id_of_Querry)
#print(link)
#alphafold.parse_pdb(link)

##3.Conservation-works but slowly
#lys.run_blast(Uniprot_id_of_Querry)
#print(lys.conservation_score(Uniprot_id_of_Querry,Lysine_positions))

##4. Files from uniprot
#print(get_from_uniprot.get_uniprot_gff(Uniprot_id_of_Querry))
#get_from_uniprot.function_site(Uniprot_id_of_Querry)
#get pdb files:
#get_from_uniprot.get_uniprot_pdb(Uniprot_id_of_Querry)

##5.Secondary structure
#print(secnd.helix_positions(Uniprot_id_of_Querry))
#print(secnd.beta_positions(Uniprot_id_of_Querry))

alphafold_annotation = format_alphafold_data(
    directory="C:/Users/friga/Desktop/VSCode/IBPproject", 
    protein_ids=Uniprot_id_of_Querry)

##END: Create a report
#pdfReportCreator.createreport(Uniprot_id_of_Querry,FASTA)
