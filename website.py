import streamlit as st
import functions as f
from stmol import showmol
import streamlit_toggle as tog

col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.write("""
    # AC3D
    *Welcome to the protein acetylation tool!*\n
    """)

blast = tog.st_toggle_switch(label="add acetylation conservation", 
                    key="blast", 
                    default_value=False, 
                    label_after = True, 
                    inactive_color = '#D3D3D3', 
                    active_color="#11567f", 
                    track_color="#29B5E8"
                    )
if blast:
    st.write('running blast may take a few minutes')

n = 94
col1, col2 = st.columns([n, 100-n])
with col1:
    Uniprot_ID = st.text_input('Give a uniprot id:', placeholder="Examples: O00115, P25665")


if Uniprot_ID != "":
    
      
    fasta = f.get_fasta(Uniprot_ID)
    st.download_button("Download fasta", fasta, file_name= Uniprot_ID+".fasta")
    
    
    if "df_calculated" not in st.session_state:
        st.session_state["df_calculated"] = False
    
    if not st.session_state.df_calculated:
        showmol(f.create_3Dobj(Uniprot_ID), width=650)
    with st.spinner('Creating report...'):
        df = f.create_reportdf(Uniprot_ID, blast)  
        if not st.session_state.df_calculated:
            st.session_state.df_calculated = True
            st.rerun()
    showmol(f.create_3Dobj(Uniprot_ID,df), width=650)
    
    st.download_button(
        label="Download report as CSV",
        data=f.df_to_csv(df),
        file_name='Report.csv',
        mime='text/csv',)
    
    show =tog.st_toggle_switch(label="show report", 
                        key="csv", 
                        default_value=False, 
                        label_after = True, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
                        )
    if show:
        st.write(df)
    
    
    

    


