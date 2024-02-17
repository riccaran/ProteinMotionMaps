# Esempio di script Python per ChimeraX per salvare immagini PNG di strutture ribbon

# Imposta i percorsi della cartella dei file PDB e della cartella di output
pdb_folder = 'C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/datasets/p16/pdbs'
output_folder = 'C:/Users/Florenzio/Desktop/test_chimera'

import os

pdb_files = ["{}/{}".format(pdb_folder, file) for file in os.listdir(pdb_folder) if file.endswith("pdb")]
files_index = {int(file.split("/")[-1].split("_")[1].split(".")[0]) : file for file in pdb_files}
pdb_files = [files_index[ind] for ind in sorted(files_index.keys())]

# Importa il modulo di ChimeraX necessario per l'esecuzione dei comandi
from chimerax.core.commands import run

run(session, f'open C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/datasets/p16/pdbs/*.pdb')
run(session, 'rainbow')
run(session, 'lighting soft')

for ind, pdb_file in enumerate(pdb_files):
    # Estrai il nome del file per usarlo nel nome dell'immagine PNG
    basename = os.path.basename(pdb_file)
    name, ext = os.path.splitext(basename)
    png_file = os.path.join(output_folder, name + '.png')

    run(session, "hide target m")
    run(session, "show #{} models".format(ind + 1))
    run(session, f'save {png_file} supersample 3')

#run C:/Users/Florenzio/Desktop/test.py
