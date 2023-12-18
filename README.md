# AC/3D Bioinformatics Tool README


## Introduction
AC/3D is a bioinformatics tool designed to provide context and 3D visualization for proteins with acetylated lysines. 


### Input Options
This tool takes as input a protein by Uniprot ID or CPLM ID (gene name can also be given, a choice between uniprot IDs can then be made).

### Output Database
The output is a database containing information about secondary structures and for the acytelated lysines: accessibility, distance to binding sites, conservation scores, known mutations.

### Platform Support
- **Backbone Dynamics:** Linux is required for supporting backbone dynamics.


## Usage

### Website Interface

To run the website interface, go to a command prompt and in the folder containing website.py type:

```bash
streamlit run website.py
```

### Commandline

If you want to use the tool directly in the commandline, you can provide a protein ID as a command-line argument. If no argument is provided, the tool will prompt you to enter the protein name or CPLM id.

```bash
python CommandLine.py [protein_id] [BLAST] [report_path]
```
- **protein_id:** The id of a protein (Uniprot id, CPLM id, or gene name).
- **BLAST (optional):** Turn on or off the calculation of conservation scores (default is True).
- **report_path (optional):** The path where the csv report should be saved. If not provided, it uses the default path (output/Report.csv).


