# -*- coding: utf-8 -*-
import os
from AC3D import PATH

#run blast and calculate conservation score based on the lysine position
from Bio.Blast import NCBIWWW, NCBIXML
from AC3D import get_from_uniprot
import logging


def run_blast(uniprot_id):
    logging.info("running blast...")
    fasta_data = get_from_uniprot.get_uniprot_fasta(uniprot_id)
    result_handle = NCBIWWW.qblast("blastp", "nr", fasta_data)
    with open(os.path.join(PATH.TEMP, f"blast_{uniprot_id}.xml"), "w") as save_file:
        save_file.write(result_handle.read())
    result_handle.close()
    logging.info("blast completed succesfully")
 

def conservation_score(uniprot_id, lysine_position):
    filename = os.path.join(PATH.TEMP, f"blast_{uniprot_id}.xml")
    with open(filename, "r") as result_file:
        blast_result = NCBIXML.read(result_file)
    conservation_list = []
    for position in lysine_position:
        lysine_count = 0
        total_number = 0
        for alignment in blast_result.alignments:
            for hsp in alignment.hsps:
                sequence = hsp.query
                if len(sequence) >= position:
                    
                    if (sequence[position - 1] == 'K'):
                        lysine_count += 1
                    total_number += 1
        conserved = lysine_count/total_number
        conservation_list.append(conserved)
    return conservation_list
               

# uniprot_id = "O00148"   
# run_blast(uniprot_id) 
# lysine_position = [32,35,333,383]        
# print(conservation_score(uniprot_id,lysine_position))   