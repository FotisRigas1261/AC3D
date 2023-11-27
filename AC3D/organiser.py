import pandas as pd
import os
import logging
from AC3D import PATH, file_parser

#This function works only if there is available data in the gff about natural variants, structures and mutations
def combine_all_data(Acc_dataframe,acetylated_lysines):

    Total_data1 = pd.merge(Acc_dataframe, acetylated_lysines, left_on='position', right_on='Acetylated Lysines', how='left')
    #Set all empty values to 0 and all non empty values of acetylated lysines to 1
    Total_data1['Conservation score'] = Total_data1['Conservation score'].fillna(0)
    Total_data1["Acetylated Lysines"] = Total_data1["Acetylated Lysines"].apply(lambda x: 1 if x>0 else 0)
    ##This part of the code also has to check if there is available information in the gff files
    #There are a lot of empty gff, or ones which only contain mutagenesis, natural variants or structures or a combination of those info
    #The parse gff will create mutations/structures/natural_variant.csv only if tis information exists 

    #1.First check for structures and intgrate them to the final data
    structure_filepath = os.path.join(PATH.TEMP, 'structures.csv')
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
        logging.warning("No information about Binding sites, Active sites or signal peptides is documented!")

    #2.Now check for available mutations
    mutations_file = os.path.join(PATH.TEMP, 'mutations.csv')
    if os.path.exists(mutations_file):
        mutations_dataframe = file_parser.parse_structures_csv(mutations_file)
        Total_data2 = pd.merge(Total_data1, mutations_dataframe, left_on='position', right_on='Position', how='left')
        # Drop the duplicate 'Position' column 
        Total_data2 = Total_data2.drop(columns=['Position'])
        #The existance of mutations is checked first, then check if also natural variants info exists
        natural_variants_file = os.path.join(PATH.TEMP, 'natural_variants.csv')
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
            Total_data2 = Total_data2.rename(columns={
                'Effect':'Mutation Effect',
                'Evidence':'Mutation Evidence'
                })
            logging.warning("No information about natural variants exist!")
            return Total_data2
    #3.Check if only natural variants and no mutations exist
    natural_variants_file = os.path.join(PATH.TEMP, 'natural_variants.csv')
    if os.path.exists(natural_variants_file) and not os.path.exists(mutations_file):
        natural_variants_dataframe = file_parser.parse_structures_csv(natural_variants_file)
        Total_data2 = pd.merge(Total_data1, natural_variants_dataframe, left_on='position', right_on='Position', how='left')
        Total_data2 = Total_data2.drop(columns=['Position'])
        Total_data2 = Total_data2.rename(columns={
                'Effect':'Variant Effect',
                'Evidence':'Variant Evidence'
                })
        logging.warning("No information about mutations exists!")
        return Total_data2
    else:
        logging.warning("No information about natural variants or mutations exists!")
        return Total_data1

#This fills the columns that we do not have information about
def ensure_uniform_format(results_dataframe):
    expected_columns = ['Function', 'Type of mutation', 'Mutation Effect', 'Mutation Evidence', 'Type of variation', 'Variant Effect', 'Variant Evidence']
    # Check if all expected columns exist in the DataFrame
    missing_columns = [column for column in expected_columns if column not in results_dataframe.columns]
    for missing_column in missing_columns:
        results_dataframe[missing_column] = 'NaN'
    # Reorder the DataFrame to match the expected column order
    results_dataframe = results_dataframe[expected_columns + [col for col in results_dataframe.columns if col not in expected_columns]]

    return results_dataframe

def clear_files():
    folder = PATH.TEMP
    files_to_delete = ["mutations.csv", "natural_variants.csv", "structures.csv","SecondaryStrAndAccessibility.csv","uniprot.gff"]
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            #also delete the xml file which is not hard coded
            if file_name.endswith(".xml"):
                os.remove(file_path)
                logging.debug(f"Deleted {file_name} (XML file)")
            elif file_name in files_to_delete:
                os.remove(file_path)
                logging.debug(f"Deleted {file_name}")
                
def integrate_backbone_dynamics(backbone_dynamics, results_dataframe):
    
    if backbone_dynamics.empty:
        return results_dataframe
    else:
        
        updated_results = pd.concat(backbone_dynamics, results_dataframe, axis=1)
        
        return(updated_results)
                
def combine_df_dict(Acc_dataframe, distances_dict, proximity_value=7):
    # Create an empty DataFrame with a 'positions' column
    distances_df = pd.DataFrame({'position': range(1, len(Acc_dataframe) + 1), 'distances': None, 'close_groups': 0})

    for key, values in distances_dict.items():
       # Fill the rows corresponding to the key with the values
       distances_df['distances'].loc[key-1] = "|".join(map(str, values))
       distances_df['close_groups'].loc[key-1] = len(list(filter(lambda x: x < proximity_value, values)))
    return pd.merge(Acc_dataframe,distances_df)
    