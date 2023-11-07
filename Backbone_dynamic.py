
import os
from b2bTools import SingleSeq
import pandas as pd
import requests


def backbone_dynamic(uniprot_id):
    base_url = "https://rest.uniprot.org/uniprotkb/"
    url = f"{base_url}{uniprot_id}.fasta"
    response = requests.get(url)
    download_directory = "/Users/wangrenkun/Documents"
    os.makedirs(download_directory, exist_ok=True)
    with open(f"{download_directory}/{uniprot_id}.fasta", 'w') as fasta_file:
        fasta_file.write(response.text)
    single_seq = SingleSeq(f"{download_directory}/{uniprot_id}.fasta")
    single_seq.predict(tools=['dynamine' ,'efoldmine'])
    all_predictions = single_seq.get_all_predictions()
    keys = list(all_predictions.keys())
    max_seq_len = max([len(pred['seq']) for pred in all_predictions.values()])
    for seq_key in keys:
        predictions = all_predictions[seq_key]
        backbone_pred = predictions['backbone']
        coil_pred = predictions['coil']
        sheet_pred = predictions['sheet']
        ppII_pred = predictions['ppII']
        helix_pred = predictions['helix']
        sidechain_pred = predictions['sidechain']
        earlyFolding_pred = predictions['earlyFolding']
        df = pd.DataFrame({'Backbone': backbone_pred,
                   'Coil': coil_pred,
                   'sheet': sheet_pred,
                   'ppII': ppII_pred,
                   'helix':helix_pred,
                   'sidechain': sidechain_pred,
                   'earlyfolding':earlyFolding_pred
                   })
        return df


result = backbone_dynamic("O00115")
print(result)