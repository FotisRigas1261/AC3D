import streamlit as st
import py3Dmol
from AC3D import get_from_uniprot, CommandLine, Querry
import requests
import re
from stmol import showmol

@st.cache_data(show_spinner=False)
def create_reportdf(Uniprot_ID, blast=False):
    return CommandLine.main(Uniprot_ID, blast)

@st.cache_data
def df_to_csv(df):
    return df.to_csv().encode('utf-8')

@st.cache_data
def get_fasta(Uniprot_ID):
    return get_from_uniprot.get_uniprot_fasta(Uniprot_ID)

@st.cache_data
def get_acetylated_lysines(Uniprot_ID):
    name, lysine_list = Querry.Querry(Uniprot_ID)
    return lysine_list

@st.cache_data
def create_3Dobj(Uniprot_ID, lysine_list=[], df=None, color_default="navy", color_alys="yellow", color_fun="purple", color_alysfun="red"):
    
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
        
        color = color_default
        position = 0
        if len(split) == 12:
            position = int(split[5]) 
        else:
            position = int(re.search('[0-9]+', split[4]).group(0))
          
        if df is not None:
            site_function = str(df["Function"].iloc[position-1])
            if site_function != "nan":
                color = color_fun
                if position in lysine_list:
                    color = color_alysfun
            elif position in lysine_list:
                color = color_alys
        elif position in lysine_list:
            color = color_alys
            
    
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

def show_protein(Uniprot_ID, df=None, show_labels=False, color_default="blue", color_alys="green", color_fun="violet", color_alysfun="orange"):

    lysine_list = get_acetylated_lysines(Uniprot_ID)
    obj = create_3Dobj(Uniprot_ID,lysine_list,df,color_default,color_alys,color_fun,color_alysfun)
    
    if show_labels:
        obj.addResLabels({'resi':lysine_list}, {'font': 'Arial', 'fontColor':'black','showBackground':False}) 
    showmol(obj, width=650)
    
    col1, col2 = st.columns([1,1])
    with col2:
        st.write("In the protein above:")
        st.write(f"acetylated lysines are :{color_alys}[{color_alys}]")
        if df is not None:
            st.write(f"functional groups are :{color_fun}[{color_fun}]")
            st.write(f"acetylated lysines in functional groups are :{color_alysfun}[{color_alysfun}]")

    
    