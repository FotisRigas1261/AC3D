import Querry as q
import Create_CPLMdf as c

print("Welcome to the protein acetylation website!\n")

#if data files do not exist yet, create them
try:
    open("CPLMids.txt","r")
    open("positions.txt","r")
except:
    c.get_CPLM_data('Acetylation.txt')
    
q.Querry()
