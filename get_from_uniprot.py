# -*- coding: utf-8 -*-


import re
import requests
import pandas as pd


#this code is to retrieve the fasta file from UniProt so the sequence and name information of the protein can be obtained by the UniProt ID
def get_uniprot_fasta(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.fasta"
    
    response = requests.get(url)
    
    if response.ok:
        return response.text
    else:
        print(f"Error retrieving data: {response.status_code}")
        return None

#uniprot_id = "P05067"
def print_data(uniprot_id):
    fasta_data = get_uniprot_fasta(uniprot_id)
    
    if fasta_data:
        print(f"Fasta data for {uniprot_id}:\n{fasta_data}")
       
    header = fasta_data.split('\n', 1)[0]
    
    
    print(header)
    
    
    
    match_species = re.search(r'OS=(\w+\s\w+)', header)
    
    if match_species:
        species = match_species.group(1)
        print(species)
    
    
    
    
    match_gene_name = re.search(r'GN=([^=\s]+)', header)
    
    if match_gene_name:
        gene_name = match_gene_name.group(1)
        print(gene_name)


# this code is for functional site(binding site) location retrieving
#The location information is stored in the gff files in UniProt, the following code could get the start and end residue number, combined with the fasta file, 
#we could get the binding site sequence and check if it is the same as the lycine acetylation location from CPLM


def get_uniprot_gff(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.gff"
    
    response = requests.get(url)
    
    if response.ok:
        return response.text
    else:
        print(f"Error retrieving data: {response.status_code}")
        return None




def function_site(uniprot_id):
    
    fasta_data = get_uniprot_fasta(uniprot_id)
    sequence = fasta_data.split('\n', 1)[1].replace("\n", "").replace("\r", "")
    gff = get_uniprot_gff(uniprot_id).splitlines()
    binding_site_lines = [line for line in gff if 'UniProtKB	Binding site' in line]
    active_site_lines = [line for line in gff if 'UniProtKB	Active site' in line]
    function_site_lines = binding_site_lines + active_site_lines
    result_list = []
    for line in function_site_lines:
        
        numbers = re.findall(r'\d+', line)
        number_list = [int(num) for num in numbers]
        result_list.append(number_list)
    
    function_site_start_location = []

    for line in result_list:
        function_site_start_location.append(line[1])

    function_site_end_location = []

    for line in result_list:
        function_site_end_location.append(line[2])
    
    
    function_site_sequence = []
    
    for n in range(len(function_site_start_location)):
        if(function_site_start_location[n] != function_site_end_location[n]):
            functional_sequence = sequence[function_site_start_location[n] - 1:function_site_end_location[n]]
        if(function_site_start_location[n] == function_site_end_location[n]):
            functional_sequence = sequence[function_site_start_location[n] - 1]
        function_site_sequence.append(functional_sequence)
        
    
    function = pd.DataFrame({'start_location': function_site_start_location, 'end_location': function_site_end_location, 'Sequence': function_site_sequence})
    return function

#print(function_site(uniprot_id))














