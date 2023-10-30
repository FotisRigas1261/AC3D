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
                #TRY to querry with genenames
                with open("../genenames.txt","r") as f:
                    d = eval(f.read())
                    try:
                        CPLMids = CPLMids + d[Querry_string]
                        if len(CPLMids) >1:
                            print('There are multiple CPLM entries matching your querry:')
                            for i in range(0, len(CPLMids)):
                                print(str(i + 1) + ". " + CPLMids[i])
                            try:
                                index = int(input("Type the number corresponding to your desired id: ".format(len(CPLMids))))
                                if 1 <= index <= len(CPLMids):
                                    item_to_keep = CPLMids[index - 1]
                                    #Add the code from CPLM querry:
                                    with open('../CPLMids.txt', 'r') as file:
                                        file_contents = file.read()
                                        #Package ast is used to handle txt files as dictionaries
                                        data_dict = ast.literal_eval(file_contents)  # Safely parse the dictionary
                                        #This creates a list which should only contain one element
                                        UniprotID_list = [key for key, value in data_dict.items() if item_to_keep in value]
                                        #Set this to querry string so that it gets returned at the end
                                        Querry_string = UniprotID_list[0]
                                    print(Querry_string)
                                else:
                                    print("Index out of bounds. Please enter a valid index.")
                            except:
                                print("Invalid input. Please enter a valid integer index.")

                                ###NEW CODE here for list containing only one id
                        if len(CPLMids)==1:
                            with open('../CPLMids.txt', 'r') as file:
                                        file_contents = file.read()
                                        #Package ast is used to handle txt files as dictionaries
                                        data_dict = ast.literal_eval(file_contents)  # Safely parse the dictionary
                                        #This creates a list which should only contain one element
                                        UniprotID_list = [key for key, value in data_dict.items() if CPLMids[0] in value]
                                        #Set this to querry string so that it gets returned at the end
                                        Querry_string = UniprotID_list[0]
                    except:
                        print("Protein not found!")

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
