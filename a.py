import os
import imageio

datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']

tot_files = list()
tot_gifs = list()
tot_frames = list()

for dataset in datasets:
    anims_dir = "output/{}/animations".format(dataset)
    anims_paths = ["{}/{}".format(anims_dir, file) for file in os.listdir(anims_dir)]
    for path_file in anims_paths:
        tot_files.append(path_file.split("/")[-1])
        gif_file = imageio.get_reader(path_file)
        tot_gifs.append(gif_file)
        frames = gif_file.get_length()
        tot_frames.append(frames)

for file, gif, frame in zip(tot_files, tot_gifs, tot_frames):
    if frame == 1:
        print(file)
