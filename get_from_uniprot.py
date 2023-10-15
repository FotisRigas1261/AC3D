# -*- coding: utf-8 -*-


import re
import requests


#this code is to retrieve the fasta file from uniprot so the sequence and name information of the protein could be obtained by the uniprot ID
def get_uniprot_fasta(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.fasta"
    
    response = requests.get(url)
    
    if response.ok:
        return response.text
    else:
        print(f"Error retrieving data: {response.status_code}")
        return None

uniprot_id = "P05067"
fasta_data = get_uniprot_fasta(uniprot_id)

if fasta_data:
    print(f"Fasta data for {uniprot_id}:\n{fasta_data}")
   
header = header = fasta_data.split('\n', 1)[0]


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
#The location information is stored in the gff files in uniprot, the following code could get the start and end residue number, combined with the fasta file, 
#we could get the bindind site sequence and check if it is the same with the lycine acetylation location got from CPLM


def get_uniprot_gff(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.gff"
    
    response = requests.get(url)
    
    if response.ok:
        return response.text
    else:
        print(f"Error retrieving data: {response.status_code}")
        return None




gff = get_uniprot_gff(uniprot_id).splitlines()




print(gff[10])# just test if the gff file could be converted into txt for further query


binding_site_lines = [line for line in gff if 'UniProtKB	Binding site' in line]
active_site_lines = [line for line in gff if 'UniProtKB	Active site' in line]

function_site_lines = binding_site_lines + active_site_lines



print(function_site_lines[3])

result_list = []
for line in function_site_lines:
    
    numbers = re.findall(r'\d+', line)
    number_list = [int(num) for num in numbers]
    result_list.append(number_list)

    
print(result_list)

function_site_start_location = []

for line in result_list:
    function_site_start_location.append(line[1])


print(function_site_start_location)


function_site_end_location = []

for line in result_list:
    function_site_end_location.append(line[2])


print(function_site_end_location)














