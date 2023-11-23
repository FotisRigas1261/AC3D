# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 20:51:21 2023

@author: 10356
"""

import streamlit as st
import pandas as pd
df = pd.read_csv('D:/output.csv')



st.title("Protein residue query")


search_number = st.number_input("Enter a row number:", min_value=0, max_value=len(df), step=1, value=0)

def backbone_categorize(value):
    if value > 1.0:
        return "membrane spanning regions"
    elif value >= 0.8:
        return "rigid"
    elif 0.69 <= value <= 0.8:
        return "rigid or flexible"
    elif value < 0.69:
        return "flexible"
    else:
        return "Uncategorized"




if st.button("Search"):
    amino_acid = df.loc[search_number-1, 'AA']
    secondary_structure = ""
    if df.loc[search_number - 1, 'BEND'] == 1:
        secondary_structure = "Secondary structure: BEND"
    elif df.loc[search_number - 1, 'HELX'] == 1:
        secondary_structure = "Secondary structure: HELX"
    elif df.loc[search_number - 1, 'STRN'] == 1:
        secondary_structure = "Secondary structure: STRN"
    elif df.loc[search_number - 1, 'TURN'] == 1:
        secondary_structure = "Secondary structure: TURN"
    elif df.loc[search_number - 1, 'unstructured'] == 1:
        secondary_structure = "Secondary structure: unstructured"
    accessibility = "high accessibility" if df.loc[search_number-1, 'high_acc_5'] == 1 else "low accessibility"
    IDR = "Within" if df.loc[search_number-1, 'IDR'] == 1 else "outof"
    backbone_value = df.loc[search_number - 1, 'Backbone']
    backbone_dynamic = backbone_categorize(backbone_value)
    sidechain = df.loc[search_number - 1, 'sidechain']
    Earlyfolding = "likely to start the protein folding process" if df.loc[search_number-1, 'earlyfolding'] >= 0.169 else "no protein folding process"

    st.write(f"Residue {search_number}:")
    st.write(f"Amino Acid Type: {amino_acid}")
    st.write(secondary_structure)
    st.write(f"Accessibility: {accessibility}")
    st.write(f"intrinsic disorder region: {IDR}")
    st.write(f"Backbone_dynamic: {backbone_dynamic}")
    st.write(f"Sidechain: {sidechain}")
    st.write(f"Earlyfolding: {Earlyfolding}")



if __name__ == "__main__":
    main()
