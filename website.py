import streamlit as st
import functions as f
from stmol import showmol
 
st.write("""
# AC3D
*Welcome to the protein acetylation tool!*
""")

Uniprot_ID = st.text_input('Give a uniprot id:', placeholder="Examples: O00115, P25665")


if Uniprot_ID != "":
    st.write('Chosen id: ', Uniprot_ID)
    
    showmol(f.create_3Dobj(Uniprot_ID))
      
    fasta = f.get_fasta(Uniprot_ID)
    st.download_button("Download fasta", fasta, file_name= Uniprot_ID+".fasta")
    
    with st.spinner('Creating report...'):
        csv = f.create_report(Uniprot_ID)    
    st.download_button(
        label="Download report as CSV",
        data=csv,
        file_name='Report.csv',
        mime='text/csv',
)
    


