import os
import time
from AC3D import PATH, CommandLine
import traceback

def run_CommandLine(key):
    try:
        CommandLine.main(key, False)
        return key, True
    except Exception as e:
        traceback_str = traceback.format_exc()
        return key, False, e, traceback_str
    
def test_all(x=1):
    with open(os.path.join(PATH.PATH().data_path, "CPLMids.txt"), "r") as f:
        idsdict = eval(f.read())
        total = len(idsdict)
        succes = 0
        errors = []

        file_path = "testoutput.txt"
        start_time = time.time()

        for n, key in enumerate(idsdict.keys(), start=1):
            print(f"{n}/{total}: {key}", flush=True)
            if n >= x and key.split("-")[0] == key:
                try:
                    result = run_CommandLine(key)
                    if not result[1]:
                        errors.append(key)

                    # Calculate estimated remaining time based on completion percentage
                    completion_percentage = (n-x) / (total-x)
                    remaining_time = (time.time() - start_time) / completion_percentage - (time.time() - start_time)
                    print(f"Estimated remaining time: {int(remaining_time) // 3600} hours, {(int(remaining_time) % 3600) // 60} minutes, {int(remaining_time) % 60} seconds", flush=True)

                    # Write the key to the file only when an error occurs
                    if not result[1]:
                        with open(file_path, 'a') as file:
                            file.write(str(key) + '\n')

                except Exception as e:
                    print(f"An error occurred for key {key}: {e}", flush=True)
                    errors.append(key)

        runs = succes + len(errors)
        print(f"succes/runs: {succes}/{runs}")

        
def test_errors():
    file_path = "testoutput.txt"
    output_keys = []

    with open(file_path, 'r') as file:
        output_keys = [line.strip() for line in file]

    for n, key in enumerate(output_keys, start=1):
        print(f"{n}/{len(output_keys)}: {key}")
        try:
            result = run_CommandLine(key)
            if result[1]:
                # Remove the key from the file when no error occurs
                with open(file_path, 'w') as file:
                    file.write('\n'.join(k for k in output_keys if k != key))
            else:
                if "No objects to concatenate" not in str(result[2]) and\
                "All arrays must be of the same length" not in str(result[2]) and\
                "'_atom_site.pdbx_sifts_xref_db_acc'" not in str(result[2]) and\
                "Empty file." not in str(result[2]):
                    raise Exception(f"An error occurred for key {key}: {result[2]}\n{result[3]}")

        except:
            traceback.print_exc()  # This will print the traceback information
            break




if __name__ == "__main__":
    #test_all(18807)
    #test_errors()
        
        #not fixed all in accessiblity.py line 38
        #CommandLine.main("O00139-2", False) #accessibiltity, No objects to concatenate
        CommandLine.main("O08550", False) #accessibility, No objects to concatenate
        #CommandLine.main("P0CE54", False) #accessibility, All arrays must be of the same length
        #CommandLine.main("P0CE55", False) #accessibility, '_atom_site.pdbx_sifts_xref_db_acc'
        #CommandLine.main("P0CE57", False) #accessibility, Empty file.
        #CommandLine.main("", False) 
        #CommandLine.main("", False) 
        #CommandLine.main("", False) 
        #CommandLine.main("", False) 
        
        #fixed
        #CommandLine.main("O00203", False) #type of mutation
        #CommandLine.main("O00422", False) #distances
        #CommandLine.main("O00757", False) #mutation evidence
        #CommandLine.main("O01666", False) #empty gff line -> no filtered structure dataframe
    
        #CommandLine.main("", False) 