# -*- coding: utf-8 -*-

# direct retrieve pdb file

from Bio import PDB
import pandas as pd
import requests
from io import StringIO

def parse_pdb(pdb_file_path):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure('protein', pdb_file_path)

    data = {'atom_number': [], 'atom_name': [], 'residue_name': [], 'chain_id': [], 'residue_number': [], 'x': [], 'y': [], 'z': []}

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    data['atom_number'].append(atom.serial_number)
                    data['atom_name'].append(atom.name)
                    data['residue_name'].append(residue.resname)
                    data['chain_id'].append(chain.id)
                    data['residue_number'].append(residue.id[1])
                    data['x'].append(atom.coord[0])
                    data['y'].append(atom.coord[1])
                    data['z'].append(atom.coord[2])

    df = pd.DataFrame(data)
    return df


pdb_file_path = '4ZWI.pdb'
pdb_dataframe = parse_pdb(pdb_file_path)
pdb_text = pdb_dataframe.to_string(index=False)
pdb_dataframe.to_csv('pdb_data.csv', index=False)
print(pdb_dataframe.head())

#link uniprot ID to pdb dataframe
uniprot_id = "P05067"

def get_alphafold_download_link(uniprot_id):
	link_pattern = 'https://alphafold.ebi.ac.uk/files/AF-{}-F1-model_v2.pdb'
	return link_pattern.format(uniprot_id)


pdb_link = get_alphafold_download_link(uniprot_id)


response = requests.get(pdb_link)
pdb_data = response.text


columns = ['atom', 'atom_number', 'atom_name', 'residue_name', 'chain_id', 'residue_number', 'x', 'y', 'z', 'occupancy', 'temperature_factor', 'element']
data = []

for line in pdb_data.split('\n'):
    if line.startswith('ATOM'):
        values = [line[0:6].strip(), int(line[6:11]), line[12:16].strip(), line[17:20].strip(),
                  line[21], int(line[22:26]), float(line[30:38]), float(line[38:46]), float(line[46:54]),
                  float(line[54:60]), float(line[60:66]), line[76:78].strip()]
        data.append(values)

df = pd.DataFrame(data, columns=columns)

print(df.head())


































