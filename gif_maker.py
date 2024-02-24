# pip install imageio
# pip install imageio[pyav]

print("Importing libraries")

import os
import shutil
import numpy as np
from PIL import Image
import imageio

print("Defining functions")

def make_folder(folde_name):
    if not os.path.exists(folde_name):
        os.makedirs(folde_name)

def remove_temp(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

print("Starting job")

datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']
int_types = ['VDW', 'HBOND', 'PIPISTACK', 'SSBOND', 'IONIC', 'PICATION']

c = 1
tot = len(datasets) * len(int_types)

for dataset in datasets:
    make_folder("output/{}/animations".format(dataset))
    
    moldyn_folder = "output/{}/moldyn_imgs".format(dataset)
    moldym_files = {int(file.split("_")[-1].split(".")[0]) : file for file in os.listdir(moldyn_folder)}
    moldym_files = ["{}/{}".format(moldyn_folder, moldym_files[ind]) for ind in sorted(moldym_files.keys())]
    moldym_images = [Image.open(image) for image in moldym_files]
    moldym_images[0].save(
        'output/{}/moldyn.gif'.format(dataset),
        save_all = True,
        append_images = moldym_images[1:],
        optimize = False,
        duration = 100,
        loop = 0
        )
    
    for int_type in int_types:
        # GIF maker
        contact_folder = "output/{}/contacts_imgs/{}".format(dataset, int_type)
        contact_files = {int(file.split("_")[-1].split(".")[0]) : file for file in os.listdir(contact_folder)}
        contact_files = ["{}/{}".format(contact_folder, contact_files[ind]) for ind in sorted(contact_files.keys())]
        contact_images = [Image.open(image) for image in contact_files]
        contact_images[0].save(
            'output/{}/contacts_{}.gif'.format(dataset, int_type),
            save_all = True,
            append_images = contact_images[1:],
            optimize = False,
            duration = 100,
            loop = 0
            )

        # GIF merger
        contacts_gif = imageio.get_reader("output/{}/contacts_{}.gif".format(dataset, int_type))
        moldyns_gif = imageio.get_reader("output/{}/moldyn.gif".format(dataset))
        output_path = "output/{}/animations/{}_{}.gif".format(dataset, dataset, int_type)

        number_of_frames = min(contacts_gif.get_length(), moldyns_gif.get_length())
        
        new_gif = imageio.get_writer(output_path, loop = 0)

        for frame_number in range(number_of_frames):
            img1 = contacts_gif.get_data(frame_number)
            img2 = moldyns_gif.get_data(frame_number)

            if img1.shape[2] != 4:
                img1 = np.dstack([img1, np.full(img1.shape[:2], 255, dtype=img1.dtype)])
            if img2.shape[2] != 4:
                img2 = np.dstack([img2, np.full(img2.shape[:2], 255, dtype=img2.dtype)])

            new_image = np.hstack((img1, img2))
            new_gif.append_data(new_image)

        contacts_gif.close()
        moldyns_gif.close()
        new_gif.close()

        print("{} % ({} - {})".format(round(c / tot * 100, 2), dataset, int_type))
        c += 1

print("Deleting folders")

for dataset in datasets:
    remove_temp("output/{}/moldyn.gif".format(dataset))
    remove_temp("output/{}/moldyn_imgs".format(dataset))
    remove_temp("output/{}/contacts_imgs".format(dataset))
    for int_type in int_types:
        remove_temp("output/{}/contacts_{}.gif".format(dataset, int_type))
    
