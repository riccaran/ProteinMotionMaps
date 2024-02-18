# Esempio di script Python per ChimeraX per salvare immagini PNG di strutture ribbon

datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl'] # ........

# Imposta i percorsi della cartella dei file PDB e della cartella di output
pdb_folder = 'C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/datasets/p16/pdbs'
output_folder = 'C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/test_chimera'
temp_path = "{}/temp".format(pdb_folder)

import os
import shutil

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

pdb_files = ["{}/{}".format(pdb_folder, file) for file in os.listdir(pdb_folder) if file.endswith("pdb")]

for pdb_path in pdb_files:
    pdb_file = pdb_path.split("/")[-1]
    max_l = len(str(len(pdb_files)))
    name, ext = pdb_file.split(".")
    prot_name, num_file = name.split("_")
    pdb_file_new = "{}_{}.{}".format(prot_name, num_file.rjust(max_l, '0'), ext)
    shutil.copy(pdb_path, "{}/{}".format(temp_path,pdb_file_new))

files_index = {int(file.split("/")[-1].split("_")[1].split(".")[0]) : file for file in pdb_files}
pdb_files = [files_index[ind] for ind in sorted(files_index.keys())]

# Importa il modulo di ChimeraX necessario per l'esecuzione dei comandi
from chimerax.core.commands import run

run(session, 'open {}/*.pdb'.format(temp_path))
run(session, 'rainbow')
run(session, 'lighting soft')
run(session, "view pad 0")

for ind, pdb_file in enumerate(pdb_files):
    # Estrai il nome del file per usarlo nel nome dell'immagine PNG
    basename = os.path.basename(pdb_file)
    name, ext = os.path.splitext(basename)
    png_file = os.path.join(output_folder, name + '.png')

    run(session, "hide target m")
    run(session, "show #{} models".format(ind + 1))
    #run(session, 'preset "initial styles" "space-filling (single color)"')
    #run(session, 'color byhetero')
    run(session, 'save {} supersample 3'.format(png_file))

run(session, "close session")
shutil.rmtree(temp_path)

#run C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/make_dynamics_gifs.py
