import os
import shutil
from chimerax.core.commands import run

def get_filename(folder, pdb_file):
    if folder == "antibody":
        prot_name, num_file, ext = pdb_file.split(".")

    elif folder == "cdk6_p16ink4a":
        name, ext = pdb_file.split(".")
        prot_name, num_file = name.split("A")
        prot_name += "A"

    elif folder == "frataxin":
        prot_name, num_ext = pdb_file.split(".")
        ext, num_file = num_ext.split("_")

    else:
        prot_name, num_ext = pdb_file.split("_")
        num_file, ext = num_ext.split(".")
       
    return prot_name, num_file, ext


def make_temp(folder):
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    if folder == "frataxin":
        pdb_files = ["{}/{}".format(pdb_folder, file) for file in os.listdir(pdb_folder) if file.startswith("fra")]
    else:
        pdb_files = ["{}/{}".format(pdb_folder, file) for file in os.listdir(pdb_folder) if file.endswith("pdb")]

    max_l = len(str(len(pdb_files)))

    for pdb_path in pdb_files:
        pdb_file = pdb_path.split("/")[-1]
        prot_name, num_file, ext = get_filename(folder, pdb_file)
        pdb_file_new = "{}_{}.{}".format(prot_name, num_file.rjust(max_l, '0'), ext)
        shutil.copy(pdb_path, "{}/{}".format(temp_path,pdb_file_new))


def make_moldym_frames(dataset):
    pdb_files = sorted(os.listdir(temp_path))

    run(session, 'open {}/*.pdb'.format(temp_path))
    run(session, 'rainbow')
    run(session, 'lighting soft')
    run(session, "view pad 0")

    for ind, pdb_file in enumerate(pdb_files):
        basename = os.path.basename(pdb_file)
        name, _ = os.path.splitext(basename)
        png_file = os.path.join(output_folder, name + '.png')

        run(session, "hide target m")
        run(session, "show #{} models".format(ind + 1))
        run(session, 'save {} supersample 3'.format(png_file))

    run(session, "close session")

    # Chimera X command:
    #run C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/make_dynamics_gifs.py


def remove_temp(folder):
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)


datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']

for dataset in datasets:
    pdb_folder = 'C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/datasets/{}/pdbs'.format(dataset)
    output_folder = 'C:/Users/Florenzio/Desktop/github_desktop/structural_bioinformatics/output/{}/moldyn_imgs'.format(dataset)
    #pdb_folder = 'datasets/{}/pdbs'.format(dataset)
    #output_folder = 'output/{}/moldyn_imgs'.format(dataset)
    temp_path = "{}/temp".format(pdb_folder)
    
    make_temp(dataset)
    make_moldym_frames(dataset)
    remove_temp(dataset)
