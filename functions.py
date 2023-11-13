import streamlit as st
from stmol import add_hover, render_pdb_resi
import py3Dmol
from AC3D import get_from_uniprot, CommandLine, Querry

@st.cache_data
def create_report(Uniprot_ID):
    return CommandLine.main(Uniprot_ID).to_csv().encode('utf-8')

@st.cache_data
def get_fasta(Uniprot_ID):
    return get_from_uniprot.get_uniprot_fasta(Uniprot_ID)

@st.cache_data
def create_3Dobj(Uniprot_ID):
    
    name, lysine_list = Querry.Querry(Uniprot_ID)
    
    pdb_link = f'https://alphafold.ebi.ac.uk/files/AF-{Uniprot_ID}-F1-model_v4.pdb'
    obj = py3Dmol.view(query=f'url:{pdb_link}') 
    add_hover(obj)
    obj.setStyle({ "cartoon": {
        "color": "spectrum",
        "colorReverse": True,
        "colorScale": "RdYlGn",
        "colorScheme": "Polarity",
        "colorBy": "resname",
            }})
    
    return render_pdb_resi(obj,resi_lst = lysine_list)
    