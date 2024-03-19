# Necessary packages, required for image processing and creating GIFs.

# pip install imageio
# pip install imageio[pyav]

print("Importing libraries")

import os
import shutil
import numpy as np
import imageio.v2 as imageio

print("Defining functions")

def make_folder(folde_name):
    """
    Create a folder if it does not exist.
    
    Parameters:
    - folder_name: The name of the folder to create.
    """
    if not os.path.exists(folde_name):
        os.makedirs(folde_name)

def remove_temp(path):
    """
    Remove a directory and all its contents.
    
    Parameters:
    - path: The file path of the directory to remove.
    """
    if os.path.exists(path):
        shutil.rmtree(path)

def make_gif(cont_folder, dyn_folder):
    cont_folder_imgs = sorted(os.listdir(cont_folder))
    dyn_folder_imgs = sorted(os.listdir(dyn_folder))

    side_by_side_imgs = list()

    for cont, dyn in zip(cont_folder_imgs, dyn_folder_imgs):
        cont_img = imageio.imread("{}/{}".format(cont_folder, cont))
        dyn_img = imageio.imread("{}/{}".format(dyn_folder, dyn))

        cont_img = cont_img[..., :3]
                
        comb_img = np.concatenate((cont_img, dyn_img), axis = 1)

        side_by_side_imgs.append(comb_img)

    imageio.mimsave(
        "output/{}/animations/{}_{}.gif".format(dataset, dataset, int_type),
        side_by_side_imgs,
        fps = 10,
        loop = 0
        )


if __name__ == "__main__":
    print("Starting job")
    
    datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']
    int_types = ['VDW', 'HBOND', 'PIPISTACK', 'SSBOND', 'IONIC', 'PICATION']
    '''
    c = 1
    tot = len(datasets) * len(int_types)

    for dataset in datasets:
        for int_type in int_types:
            make_folder("output/{}/animations".format(dataset))

            cont_folder = "output/{}/contacts_imgs/{}".format(dataset, int_type)
            dyn_folder = "output/{}/moldyn_imgs".format(dataset)

            make_gif(cont_folder, dyn_folder)

            print("{} % ({} - {})".format(round(c / tot * 100, 2), dataset, int_type))
            c += 1

    print("Deleting folders")
    '''
    for dataset in datasets:
        remove_temp("output/{}/moldyn_imgs".format(dataset))
        remove_temp("output/{}/contacts_imgs".format(dataset))
