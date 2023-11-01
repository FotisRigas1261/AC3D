import pandas as pd
import os

def combine_all_data(Acc_dataframe,acetylated_lysines,structures_dataframe,mutations_dataframe,natural_variants_dataframe):
    Total_data1 = pd.merge(Acc_dataframe, acetylated_lysines, left_on='position', right_on='Acetylated Lysines', how='left')
    #Set all empty values to 0 and all non empty values of acetylated lysines to 1
    Total_data1['Conservation score'] = Total_data1['Conservation score'].fillna(0)

    #Only keep active sites, binding sites and signal peptides
    mask = (structures_dataframe['Structure'] == 'Active site') | (structures_dataframe['Structure'] == 'Signal peptide') | (structures_dataframe['Structure'] == 'Binding site')
    filtered_Structure=structures_dataframe[mask].copy()

    # Create the 'Function' column with 'Structure'
    filtered_Structure['Function'] = filtered_Structure['Structure']

    # Combine the structure and Total1df
    for index, row in filtered_Structure.iterrows():
        start_pos = row['Start position']
        end_pos = row['End position']
        function = row['Function']
        Total_data1.loc[(Total_data1['position'] >= start_pos) & (Total_data1['position'] <= end_pos), 'Function'] = function

    #Combine mutations and natural variants
    Total_data2 = pd.merge(Total_data1, mutations_dataframe, left_on='position', right_on='Position', how='left')
    # Drop the duplicate 'Position' column if needed
    Total_data2 = Total_data2.drop(columns=['Position'])

    #Combine natural variants
    Total_data3 = pd.merge(Total_data2, natural_variants_dataframe, left_on='position', right_on='Position', how='left')
    Total_data3 = Total_data3.drop(columns=['Position'])

    Total_data3 = Total_data3.rename(columns={
        'Effect_x':'Mutation Effect',
        'Evidence_x':'Mutation Evidence',
        'Effect_y':'Variant Effect',
        'Evidence_y':'Variant Evidence'
    })

    return Total_data3

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