# IBPproject
Lysine Acetylation Website
From here, dowanload the Acetylation data so that the database on which the code is based is created, it is too large to upload here:
(https://cplm.biocuckoo.cn/Download.php)https://cplm.biocuckoo.cn/Download.php
select the acetylation dataset fro the second table

# Things to be done (as of my understanding)
For each of the acetylation sites that can be found in the cplm database:

From UniProt: functional information

-Is the acetylated lysine known as functional site?

-Is the acetylated lysine near a residue known as functional site? (Both in primary and tertiary sequence)

From AlphaFold database: structural information

-With structureMap, get Secondary structure of residues

-Accessibility of residues Whether the residue is in an intrinsically disordered region

-With dynaMine, get Information on the backbone dynamics

Basically if someone querries a specific protein plus a specific residue, they should get information on all of the above.
This information cannot be found into the CPLM database so we might need to connect to the APIs of Uniprot and Alpha fold
(i don't know how to do this but i guess we will find a way)


Work from 16/10 to 23/10:

1. Integrate the functions([1]from CPLM txt file parse the CPLM ID, Uniprot ID, genename, acetylation position; [2] from Uniprot parse the Uniprot ID, function sites location and sequence, lysine acetylation distance to function site(0aa if in the sequence),secondary structure information(location and sequence),[3] from Alphafold parse the PDB file of the 3D localization information of atoms and residues(Other information needed for 3D visualization is being searched)).

2. An uniorm input(CPLM ID, Uniprot ID, and Gene name) start from the CPLM database.
3. How to operate lysine acetylation conservation calculation(what sequence comparison )
4. 3D visualization method implemented in python(highlight the lysine acetylation in 3D)


