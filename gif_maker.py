import os
from PIL import Image

datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']

for dataset in datasets:
    contact_folder = "output/{}/contacts_imgs".format(dataset)
    moldyn_folder = "output/{}/moldyn_imgs".format(dataset)

    contact_files = {int(file.split("_")[-1].split(".")[0]) : file for file in os.listdir(contact_folder)}
    moldym_files = {int(file.split("_")[-1].split(".")[0]) : file for file in os.listdir(moldyn_folder)}

    contact_files = ["{}/{}".format(contact_folder, contact_files[ind]) for ind in sorted(contact_files.keys())]
    moldym_files = ["{}/{}".format(moldyn_folder, moldym_files[ind]) for ind in sorted(moldym_files.keys())]

    # PNG images upload
    contact_images = [Image.open(image) for image in contact_files]
    moldym_images = [Image.open(image) for image in moldym_files]

    # GIF making
    contact_images[0].save('output/{}/contacts.gif'.format(dataset),
                           save_all = True,
                           append_images = contact_images[1:],
                           optimize = False,
                           duration = 100,
                           loop = 0)

    moldym_images[0].save('output/{}/moldyn.gif'.format(dataset),
                          save_all = True,
                          append_images = moldym_images[1:],
                          optimize = False,
                          duration = 100,
                          loop = 0)
