import ast
import logging
import os
from AC3D import PATH
import AC3D.Create_CPLMdf as c

def Querry(Querry_string):
    """
    Fetches data concerning acetylated lysines, processes the data, and returns Uniprot ID and acetylation positions.

    Parameters
    ----------
    Querry_string : str
        The ID of a protein, which can be a CPLM ID, Uniprot ID, or gene name.

    Returns
    -------
    tuple
        A tuple containing the Uniprot ID and a list of acetylation positions.
    """

    # If data files do not exist yet, create them
    try:
        open(os.path.join(PATH.PATH().data_path, "CPLMids.txt"), "r")
        open(os.path.join(PATH.PATH().data_path, "positions.txt"), "r")
        open(os.path.join(PATH.PATH().data_path, "genenames.txt"), "r")
    except:
        c.get_CPLM_data(os.path.join(PATH.PATH().data_path, 'Acetylation.txt'))

    CPLMids = []
    if not Querry_string.startswith("CPLM"):
        with open(os.path.join(PATH.PATH().data_path, "CPLMids.txt"), "r") as f:
            d = eval(f.read())
            try:
                CPLMids = CPLMids + d[Querry_string]
            except:
                # TRY to query with gene names
                with open(os.path.join(PATH.PATH().data_path, "genenames.txt"), "r") as f:
                    d = eval(f.read())
                    try:
                        CPLMids = CPLMids + d[Querry_string]

                        UniprotID_list = []
                        with open(os.path.join(PATH.PATH().data_path, "CPLMids.txt"), 'r') as file:
                            file_contents = file.read()
                            # Package ast is used to handle txt files as dictionaries
                            data_dict = ast.literal_eval(file_contents)  # Safely parse the dictionary
                            # This creates a list that should only contain one element
                            for CPLMid in CPLMids:
                                UniprotID_list.extend([key for key, value in data_dict.items() if CPLMid in value])

                            if len(CPLMids) > 1:
                                entries = ""
                                for i in range(0, len(CPLMids)):
                                    entries = entries + str(i + 1) + ". " + UniprotID_list[i] + "\n"
                                logging.info('There are multiple CPLM entries matching your query:\n' + entries)

                                try:
                                    index = int(input("Type the number corresponding to your desired id: ".format(len(CPLMids))))
                                    if 1 <= index <= len(CPLMids):
                                        Querry_string = UniprotID_list[index - 1]
                                        logging.debug(Querry_string)
                                    else:
                                        logging.error("Index out of bounds. Please enter a valid index.")
                                except:
                                    logging.error("Invalid input. Please enter a valid integer index.")

                                    # NEW CODE here for a list containing only one id
                            if len(CPLMids) == 1:
                                # Set this to the query string so that it gets returned at the end
                                Querry_string = UniprotID_list[0]
                    except:
                        logging.error("Protein not found!")

    else:
        try:
            CPLMids.append(Querry_string)
        except:
            logging.error("CPLM id not found")

    positions = []
    with open(os.path.join(PATH.PATH().data_path, "positions.txt"), "r") as f:
        d = eval(f.read())
        for CPLMid in CPLMids:
            positions = positions + d[CPLMid]

    logging.info("This protein has acetylations at positions:\n" + ", ".join(map(str, positions)))

    # This part of the function is made for the query to always return Uniprot IDs
    if Querry_string.startswith("CPLM"):
        with open(os.path.join(PATH.PATH().data_path, "CPLMids.txt"), 'r') as file:
            file_contents = file.read()
            # Package ast is used to handle txt files as dictionaries
            data_dict = ast.literal_eval(file_contents)  # Safely parse the dictionary
            # This creates a list that should only contain one element
            UniprotID_list = [key for key, value in data_dict.items() if Querry_string in value]
            UniprotID = UniprotID_list[0]
            print(UniprotID)
            return UniprotID, positions

    else:
        # In this case, the query is already the Uniprot ID
        return Querry_string, positions

