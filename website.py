import streamlit as st
import functions as f
import streamlit_toggle as tog
import platform
import structure_circle
import residue_query_box

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
    
    show_labels = tog.st_toggle_switch(label="show acetylated lysine labels", 
                        key="label", 
                        default_value=False, 
                        label_after = True, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
                        )
    
    if "df_calculated" not in st.session_state:
        st.session_state["df_calculated"] = False
    if not st.session_state.df_calculated:
        f.show_protein(Uniprot_ID, show_labels=show_labels)
        
    with st.spinner('Creating report...'):
        df = f.create_reportdf(Uniprot_ID, blast)  
        if not st.session_state.df_calculated:
            st.session_state.df_calculated = True
            st.rerun()
    f.show_protein(Uniprot_ID, df, show_labels=show_labels)
    
    st.download_button(
        label="Download report as CSV",
        data=f.df_to_csv(df),
        file_name='Report.csv',
        mime='text/csv',)
    
    show_report = tog.st_toggle_switch(label="show report", 
                        key="csv", 
                        default_value=False, 
                        label_after = True, 
                        inactive_color = '#D3D3D3', 
                        active_color="#11567f", 
                        track_color="#29B5E8"
                        )
    if show_report:
        st.write(df)
    
    os_name = platform.system()
    if os_name == 'Linux' or os_name == 'Darwin':
        import AC3D.Backbone_dynamic as bd
        dfbd = bd.backbone_dynamic(Uniprot_ID)
        structure_circle.run(dfbd)
        residue_query_box.run(dfbd)
    else:
        st.write("The backbone dynamics can't be shown on your operating system!")
        st.write("Your operating system is ", os_name)


