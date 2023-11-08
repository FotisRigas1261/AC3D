import re
import requests
import pandas as pd
import logging
import os
import PATH


#this code is to retrieve the fasta file from UniProt so the sequence and name information of the protein can be obtained by the UniProt ID
def get_uniprot_fasta(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.fasta"
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        logging.error(f"Error retrieving data: {response.status_code}")
        return None

def get_uniprot_gff(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.gff"
    
    response = requests.get(url)
    
    if response.ok:
        gff_file_path = os.path.join(PATH.TEMP, 'uniprot.gff')
        with open(gff_file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

    else:
        logging.error(f"Error retrieving data: {response.status_code}")




    












