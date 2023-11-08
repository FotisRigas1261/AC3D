# -*- coding: utf-8 -*-
import requests
import re
import pandas as pd
import logging

def helix_positions(uniprot_id):
    
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        pattern = r'"type":"Helix","location":{"start":{"value":(\d+),"modifier":"EXACT"},"end":{"value":(\d+),"modifier":"EXACT"}}'
        matches = re.findall(pattern, data)
        helix_df = pd.DataFrame([(int(start), int(end)) for start, end in matches], columns=['start', 'end'])
        
        return helix_df
    else:
       
        logging.error(f"Error: Unable to retrieve data for Uniprot ID {uniprot_id}")
        return None


def beta_positions(uniprot_id):
    
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text  
        pattern = r'"type":"Beta strand","location":{"start":{"value":(\d+),"modifier":"EXACT"},"end":{"value":(\d+),"modifier":"EXACT"}}' 
        matches = re.findall(pattern, data)
        beta_df = pd.DataFrame([(int(start), int(end)) for start, end in matches], columns=['start', 'end'])
        
        return beta_df
    else:
       
        logging.error(f"Error: Unable to retrieve data for Uniprot ID {uniprot_id}")
        return None




# uniprot_id = "O00154"
# helix_df = helix_positions(uniprot_id)
# beta_df = beta_positions(uniprot_id)

# print(helix_df)
# print(beta_df)

