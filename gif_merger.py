from PIL import Image, ImageSequence

datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']

for dataset in datasets:
    contacts_gif = Image.open("output/{}/contacts.gif".format(dataset))
    moldyns_gif = Image.open("output/{}/moldyn.gif".format(dataset))
    output_path = "output/{}/animation.gif".format(dataset)

    width1, height1 = contacts_gif.size
    width2, height2 = moldyns_gif.size
    total_width = width1 + width2
    max_height = max(height1, height2)

    frames = list()

    for frame1, frame2 in zip(ImageSequence.Iterator(contacts_gif), ImageSequence.Iterator(moldyns_gif)):
        frame1 = frame1.convert('RGBA').resize((width1, max_height), Image.LANCZOS)
        frame2 = frame2.convert('RGBA').resize((width2, max_height), Image.LANCZOS)

        combined_frame = Image.new('RGBA', (total_width, max_height), "black")

        combined_frame.paste(frame1, (0, 0), frame1)
        combined_frame.paste(frame2, (width1, 0), frame2)

        frames.append(combined_frame)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=contacts_gif.info['duration'], disposal=2)
