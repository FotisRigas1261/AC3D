import pandas as pd
import os
import file_parser

#This function works only if there is available data in the gff about natural variants, structures and mutations
def combine_all_data(Acc_dataframe,acetylated_lysines):#,structures_dataframe,mutations_dataframe,natural_variants_dataframe):
    Total_data1 = pd.merge(Acc_dataframe, acetylated_lysines, left_on='position', right_on='Acetylated Lysines', how='left')
    #Set all empty values to 0 and all non empty values of acetylated lysines to 1
    Total_data1['Conservation score'] = Total_data1['Conservation score'].fillna(0)

    ##This part of the code also has to check if there is available information in the gff files
    #There are a lot of empty gff, or ones which only contain mutagenesis, natural variants or structures or a combination of those info
    #The parse gff will create mutations/structures/natural_variant.csv only if tis information exists 

    #1.First check for structures and intgrate them to the final data
    structure_filepath = 'structures.csv'
    if os.path.exists(structure_filepath):
        structures_dataframe = file_parser.parse_structures_csv(structure_filepath)

        # Create the 'Function' column with 'Structure', it better represents bindin sites etc
        structures_dataframe['Function'] = structures_dataframe['Structure']
        for index, row in structures_dataframe.iterrows():
            start_pos = row['Start position']
            end_pos = row['End position']
            function = row['Function']
            Total_data1.loc[(Total_data1['position'] >= start_pos) & (Total_data1['position'] <= end_pos), 'Function'] = function
    else:
        print("No information about Binding sites, Active sites or signal peptides is documented!")

    #2.Now check for available mutations
    mutations_file = 'mutations.csv'
    if os.path.exists(mutations_file):
        mutations_dataframe = file_parser.parse_structures_csv(mutations_file)
        Total_data2 = pd.merge(Total_data1, mutations_dataframe, left_on='position', right_on='Position', how='left')
        # Drop the duplicate 'Position' column 
        Total_data2 = Total_data2.drop(columns=['Position'])
        #The existance of mutations is checked first, then check if also natural variants info exists
        natural_variants_file = 'natural_variants.csv'
        if os.path.exists(natural_variants_file):
            natural_variants_dataframe = file_parser.parse_structures_csv(natural_variants_file)
            Total_data3 = pd.merge(Total_data2, natural_variants_dataframe, left_on='position', right_on='Position', how='left')
            Total_data3 = Total_data3.drop(columns=['Position'])
            Total_data3 = Total_data3.rename(columns={
                #The columns will automatically be titled as effect_x and effect_y because they have the same header
                'Effect_x':'Mutation Effect',
                'Evidence_x':'Mutation Evidence',
                'Effect_y':'Variant Effect',
                'Evidence_y':'Variant Evidence'
                })
            return Total_data3
        else:
            print("No information about natural variants exist!")
            return Total_data2
    #3.Check if only natural variants and no mutations exist
    natural_variants_file = 'natural_variants.csv'
    if os.path.exists(natural_variants_file) and not os.path.exists(mutations_file):
        natural_variants_dataframe = file_parser.parse_structures_csv(natural_variants_file)
        Total_data2 = pd.merge(Total_data1, natural_variants_dataframe, left_on='position', right_on='Position', how='left')
        Total_data2 = Total_data2.drop(columns=['Position'])
        print("No information about mutations exists!")
        return Total_data2
    else:
        print("No information about natural variants or mutations exists!")
        return Total_data1


def clear_files():
    current_folder = os.getcwd() 
    files_to_delete = ["mutations.csv", "natural_variants.csv", "structures.csv","SecondaryStrAndAccessibility.csv","uniprot.gff"]
    for file_name in os.listdir(current_folder):
        file_path = os.path.join(current_folder, file_name)
        if os.path.isfile(file_path):
            #also delete the xml file which is not hard coded
            if file_name.endswith(".xml"):
                os.remove(file_path)
                print(f"Deleted {file_name} (XML file)")
            elif file_name in files_to_delete:
                os.remove(file_path)
                print(f"Deleted {file_name}")
            else:
                print(f"File {file_name} not found")