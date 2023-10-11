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
