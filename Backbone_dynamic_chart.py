# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 20:51:21 2023

@author: 10356
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


bdf = pd.read_csv('D:/O00115_backbone_dynamics.csv')
rigid_threshold = 0.8
membrane_threshold = 1.0
flexible_threshold = 0.69
dependent_lower_threshold = 0.69
dependent_upper_threshold = 0.8

def categorize_region(value):
    if value > membrane_threshold:
        return "Membrane Spanning"
    elif value > rigid_threshold:
        return "Rigid"
    elif value < flexible_threshold:
        return "Flexible"
    elif dependent_lower_threshold <= value <= dependent_upper_threshold:
        return "Dependent"
    else:
        return "Unknown"


bdf['Region'] = bdf['Backbone'].apply(categorize_region)
fig, ax = plt.subplots()


ax.axhspan(0.55, flexible_threshold, color='blue', alpha=0.3, label='Flexible Region')
ax.axhspan(dependent_lower_threshold, dependent_upper_threshold, color='yellow', alpha=0.3, label='Dependent Region')
ax.axhspan(rigid_threshold, membrane_threshold, color='red', alpha=0.3, label='Membrane Spanning Region')


ax.plot(bdf.index, bdf['Backbone'], marker='o', markersize=3)


ax.set_xlabel('Residue Number')
ax.set_ylabel('Backbone Dynamic Value')
ax.set_title('Backbone Dynamics Chart')
ax.legend(fontsize='small')

st.pyplot(fig)


