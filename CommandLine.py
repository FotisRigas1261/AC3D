import Querry as q
import Create_CPLMdf as c
import sys

Querry_string = ""
if len(sys.argv) == 1:
    print("Welcome to the protein acetylation website!\n")
    Querry_string = input('Type the name of the protein you want to investigate or a CPLM id: ')
else:
    Querry_string = sys.argv[1]
    
#if data files do not exist yet, create them
try:
    open("CPLMids.txt","r")
    open("positions.txt","r")
except:
    c.get_CPLM_data('Acetylation.txt')
    
q.Querry(Querry_string)
