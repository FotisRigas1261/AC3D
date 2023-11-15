import streamlit as st
import py3Dmol
from AC3D import get_from_uniprot, CommandLine, Querry
import requests
import pandas as pd
import re

@st.cache_data
def create_reportdf(Uniprot_ID, blast=False):
    return CommandLine.main(Uniprot_ID, blast)

@st.cache_data
def df_to_csv(df):
    return df.to_csv().encode('utf-8')

@st.cache_data
def get_fasta(Uniprot_ID):
    return get_from_uniprot.get_uniprot_fasta(Uniprot_ID)

@st.cache_data
def create_3Dobj(Uniprot_ID, df=None):
    
    name, lysine_list = Querry.Querry(Uniprot_ID)
    
    pdb_link = f'https://alphafold.ebi.ac.uk/files/AF-{Uniprot_ID}-F1-model_v4.pdb'
    response = requests.get(pdb_link)
    pdb_data = response.text
        
    view = py3Dmol.view()
    view.addModelsAsFrames(pdb_data)
    
    i = 0
    for line in pdb_data.split("\n"):
        split = line.split()
        if len(split) == 0 or split[0] != "ATOM":
            continue
        
        color = "navy"
        position = 0
        if len(split) == 12:
            position = int(split[5]) 
        else:
            position = int(re.search('[0-9]+', split[4]).group(0))
          
        if df is not None:
            site_function = str(df["Function"].iloc[position-1])
            if site_function != "nan":
                color = "purple"
                if position in lysine_list:
                    color = "red"
            elif position in lysine_list:
                color = "yellow"
        elif position in lysine_list:
            color = "yellow"
            
    
        view.setStyle({'model': -1, 'serial': i+1}, {"cartoon": {'color': color}})
        i += 1
        
    backgroundColor='white'
    fontColor='black'
    js_script = """function(atom,viewer) {
                   if(!atom.label) {
                    atom.label = viewer.addLabel(atom.resn+':'+atom.resi,{position: atom, backgroundColor:"%s" , fontColor:"%s"});
                }
              }"""%(backgroundColor,fontColor)
    view.setHoverable({},True,js_script,
               """function(atom,viewer) {
                   if(atom.label) {
                    viewer.removeLabel(atom.label);
                    delete atom.label;
                   }
                }"""
               )
    view.zoomTo()
    return view
    
    