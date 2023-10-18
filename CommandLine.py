import pandas as pd
import Querry as q
import Create_CPLMdf as c

print("Welcome to the protein acetylation website!\n")

CPLM_positions = c.get_CPLM_data('Acetylation.txt')
print(CPLM_positions)
CPLM_Database = pd.read_csv('data.csv')

#print(q.Querry(CPLM_Database))
