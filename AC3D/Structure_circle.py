# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 20:51:21 2023

@author: 10356
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


df = pd.read_csv('D:/output.csv')


total_rows = len(df)


fig, ax = plt.subplots()


circle = plt.Circle((0.5, 0.5), 0.3, color='blue', fill=False)
ax.add_artist(circle)


for i, row in df.iterrows():
    if row['IDR'] == 1:
        angle_start = i / total_rows * 360
        angle_end = (i + 1) / total_rows * 360
        IDR_circle = Wedge(center=(0.5, 0.5), r=0.31, theta1=angle_start, theta2=angle_end,
                               width=0.01, fill=False, edgecolor='black', linestyle='dashed')
        ax.add_artist(IDR_circle)
        ax.text(0.05, 0.2, 'IDR', color='black', ha='left', va='center', fontsize=4)


for i, row in df.iterrows():
    if row['high_acc_5'] == 1:
        angle_start1 = i / total_rows * 360
        angle_end1 = (i + 1) / total_rows * 360
        accessible_circle = Wedge(center=(0.5, 0.5), r=0.32, theta1=angle_start1, theta2=angle_end1,
                               width=0.01, fill=False, edgecolor='green', linestyle='dashed')
        ax.add_artist(accessible_circle)
        ax.text(0.05, 0.18, 'Accessible', color='green', ha='left', va='center', fontsize=4)

cmap = LinearSegmentedColormap.from_list('my_cmap', ['blue', 'purple', 'yellow', 'red'], N=256)
for i, row in df.iterrows():
    backbone_value = row['Backbone']
    if backbone_value > 1.0:
        category_color = cmap(255)
        category_label = 'Membrane Spanning'
    elif backbone_value > 0.8:
        category_color = cmap(192)
        category_label = 'Rigid Conformations'
    elif backbone_value < 0.69:
        category_color = cmap(0)
        category_label = 'Flexible Regions'
    else:
        category_color = cmap(128)
        category_label = 'Context Dependent'

    angle_start2 = i / total_rows * 360
    angle_end2 = (i + 1) / total_rows * 360
    backbone_circle = Wedge(center=(0.5, 0.5), r=0.33, theta1=angle_start2, theta2=angle_end2,
                            width=0.01, fill=False, edgecolor=category_color, linestyle='dashed')
    ax.add_artist(backbone_circle)
    y_position = 0.16 - 0.02 * ['Membrane Spanning', 'Rigid Conformations', 'Flexible Regions', 'Context Dependent'].index(category_label)
    ax.text(0.05, y_position, category_label, color=category_color, ha='left', va='center', fontsize=4)

ax.text(0.72, 0.5, 'Origin --->', color='black', ha='center', va='center', fontsize=8)
ax.set_aspect('equal', adjustable='box')

ax.set_xticks([])
ax.set_yticks([])


ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)



st.pyplot(fig)


if __name__ == "__main__":
    main()
