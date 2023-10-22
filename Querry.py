import get_from_uniprot
import ast

def Querry(Querry_string):

    CPLMids = []
    if not Querry_string.startswith("CPLM"):
        with open("../CPLMids.txt","r") as f:
            d = eval(f.read())
            try:
                CPLMids = CPLMids + d[Querry_string]
            except:
                print("Protein name not found")
    else:
        try:
            CPLMids.append(Querry_string)
        except:
            print("CPLM id not found")
        
    
    positions = []       
    with open("../positions.txt","r") as f:
        d = eval(f.read())
        for CPLMid in CPLMids:
            positions = positions + d[CPLMid]
    
    print("This protein has acetylations at positions:")
    print(positions)
    
    
#        get_from_uniprot.print_data(Querry_string)

    #This part oif the function is made in order for the querry to always return uniprot ids
    if Querry_string.startswith("CPLM"):
        with open('../CPLMids.txt', 'r') as file:
            file_contents = file.read()
            #Package ast is used to handle txt files as dictionaries
            data_dict = ast.literal_eval(file_contents)  # Safely parse the dictionary
            #This creates a list which should only contain one element
            UniprotID_list = [key for key, value in data_dict.items() if Querry_string in value]
            UniprotID = UniprotID_list[0]
            print(UniprotID)
            return UniprotID,positions
            
    else:
        #In this case the querry is already the Uniprot ID
        return Querry_string,positions

 