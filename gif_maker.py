# PNG images upload
files_indexed = {int(file[:-4].split("_")[-1]) : file for file in os.listdir(path)}
images = [Image.open("{}/contact_maps/{}".format(folder, image)) for image in [files_indexed[file_ind] for file_ind in sorted(files_indexed.keys())]]

# GIF making
images[0].save('output.gif', save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

