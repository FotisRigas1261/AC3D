# -*- coding: utf-8 -*-
import nglview as nv


def visualization(Uniprot_ID, lysine_list):
    lysine_position = ' '.join(map(str, lysine_list))
    pdb_link = f'https://alphafold.ebi.ac.uk/files/AF-{Uniprot_ID}-F1-model_v2.pdb'
    view = nv.show_url(pdb_link, default_representation=False)
    view.add_cartoon(color='blue')
    view.add_surface(lysine_position, color='red',radius = 0.05)
    view.center()
    display(view)

lysine_list = [55,80,106]
Uniprot_ID = "O15552"
visualization(Uniprot_ID, lysine_list)












