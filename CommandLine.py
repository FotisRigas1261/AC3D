import pandas as pd
import Querry as q

print("Welcome to the protein acetylation website!\n")

CPLM_Database = pd.read_csv('C:/Users/friga/Desktop/VSCode/data.csv')

print(q.Querry(CPLM_Database))
