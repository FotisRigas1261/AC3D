import os
import time
from AC3D import PATH, CommandLine

def run_CommandLine(key):
    try:
        CommandLine.main(key, False)
        return key, True
    except Exception as e:
        return key, False, e
    
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
        for line in file:
            output_keys.append(line.strip())

    total = len(output_keys)
    succes = 0
    errors = []

    for n, key in enumerate(output_keys, start=1):
        print(f"{n}/{total}: {key}")
        try:
            result = run_CommandLine(key)
            if result[1]:
                succes += 1
            else:
                errors.append((key, result[2]))

        except Exception as e:
            print(f"An error occurred for key {key}: {e}")
            errors.append((key, e))

    runs = succes + len(errors)
    print(f"succes/runs: {succes}/{runs}")


if __name__ == "__main__":
    test_all(2064)
        
        #not fixed
        #CommandLine.main("O00139-2", False) #accessibiltity 
        #CommandLine.main("O08550", False) #accessibility
        #CommandLine.main("O08710", False) 
        #CommandLine.main("O14686", False) 
        #CommandLine.main("O15018", False) 
        #CommandLine.main("O15050", False) 
        #CommandLine.main("O15078", False) 
        #CommandLine.main("O15417", False) 
        #CommandLine.main("", False) 
        
        #fixed
        #CommandLine.main("O00203", False) #type of mutation
        #CommandLine.main("O00422", False) #distances
        #CommandLine.main("O00757", False) #mutation evidence
        #CommandLine.main("O01666", False) #empty gff line -> no filtered structure dataframe
    
        #CommandLine.main("", False) 