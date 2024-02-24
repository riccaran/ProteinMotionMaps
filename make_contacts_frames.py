print("Importing libraries")
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("Defining functions")

def make_folder(folde_name):
    if not os.path.exists(folde_name):
        os.makedirs(folde_name)

def files_indexer(dataset):
    datasets_edges = dict()
    edges_files = [file for file in os.listdir(edge_folder) if file.endswith("Edges")]
        
    if dataset == "antibody":
        files_index = {int(file.split(".")[1]) : file for file in edges_files}
        
    elif dataset == "cdk6_p16ink4a":
        files_index = {int(file.split("A")[1].split(".")[0]) : file for file in edges_files}

    elif dataset == "frataxin":
        files_index = {int(file.split("_")[1]) : file for file in edges_files}
    
    else:
        files_index = {int(file.split("_")[1].split(".")[0]) : file for file in edges_files}

    edges_files = ["{}/{}".format(edge_folder, files_index[index]) for index in sorted(files_index.keys())]

    return edges_files

def process_df(data):
    for ind, node_cols in enumerate(["NodeId1", "NodeId2"]):
        split_cols = data[node_cols].str.replace("_:", "").str.split(':', expand=True)
        if split_cols.shape[1] > 2:
            data[['chain_{}'.format(ind + 1), 'id_{}'.format(ind + 1), 'aa_{}'.format(ind + 1)]] = split_cols
        else:
            data[['id_{}'.format(ind + 1), 'aa_{}'.format(ind + 1)]] = split_cols

    data[['id_1', 'id_2']] = data[['id_1', 'id_2']].astype(int)
    data[['int_type', 'int_portion']] = data['Interaction'].str.split(':', expand=True)

    data.drop(['NodeId1', 'NodeId2', 'Interaction'], axis=1, inplace=True)

    data = data.rename(columns = {
        "Distance" : "distance",
        "Angle" : "angle",
        "Energy" : "energy",
        "Atom1" : "atom1",
        "Atom2" : "atom2",
        "Donor" : "donor",
        "Positive" : "positive",
        "Cation" : "cation",
        "Orientation" : "orientation",
    })

    if ("chain_1" in data.columns) and ("chain_2" in data.columns):
        rin = data[["chain_1", "chain_2", "aa_1", "aa_2",  "id_1",  "id_2",  "int_type",  "int_portion",  "distance",  "angle",  "energy",  "atom1",  "atom2"]]
    elif "chain_1" in data.columns:
        rin = data[["chain_1", "aa_1", "aa_2",  "id_1",  "id_2",  "int_type",  "int_portion",  "distance",  "angle",  "energy",  "atom1",  "atom2"]]
    elif "chain_2" in data.columns:
        rin = data[["chain_2", "aa_1", "aa_2",  "id_1",  "id_2",  "int_type",  "int_portion",  "distance",  "angle",  "energy",  "atom1",  "atom2"]]
    else:
        rin = data[["aa_1", "aa_2",  "id_1",  "id_2",  "int_type",  "int_portion",  "distance",  "angle",  "energy",  "atom1",  "atom2"]]

    suppl = data[["donor", "positive", "cation", "orientation"]]

    return rin, suppl

def plot_contact_map(data, int_type, path_save, v_min, v_max, min_id, max_id):
    filtered_data = data[data['int_type'] == int_type]
    
    contact_matrix = np.full((max_id - min_id + 1, max_id - min_id + 1), np.nan)

    for _, row in filtered_data.iterrows():
        i, j = row['id_1'] - min_id - 1, row['id_2'] - min_id - 1
        if i < contact_matrix.shape[0] and j < contact_matrix.shape[1]:
            contact_matrix[i, j] = row['distance']
            contact_matrix[j, i] = row['distance']

    plt.style.use('dark_background')
    cmap = plt.cm.inferno.reversed()

    plt.figure(figsize=(10, 8))
    im = plt.imshow(contact_matrix, cmap=cmap, interpolation='none', vmin=v_min, vmax=v_max)
    plt.colorbar(im, label='Distance (Å)')
    plt.title("{} contact map".format(int_type))

    ticks = np.arange(min_id, max_id + 1)
    tick_positions = np.arange(0, max_id - min_id + 1, 15)
    tick_labels = np.arange(min_id, max_id + 1, 15)
    plt.xticks(tick_positions, tick_labels)
    plt.yticks(tick_positions, tick_labels)

    plt.savefig(path_save, dpi = 100, transparent = False)
    plt.close()

def get_filename(folder, pdb_file):
    if folder == "antibody":
        prot_name, num_file, ext = pdb_file.split(".")

    elif folder == "cdk6_p16ink4a":
        num_name, ext = pdb_file.split(".")
        prot_name, num_file = num_name.split("A")
        prot_name += "A"

    elif folder == "frataxin":
        prot_name, num_ext = pdb_file.split(".")
        ext_1, num_file, ext_2 = num_ext.split("_")
        ext = ext_1 + "_" + ext_2

    else:
        num_name, ext = pdb_file.split(".")
        prot_name, num_file = num_name.split("_")
       
    return prot_name, num_file, ext

def make_seq_range(edges_files):
    v_min = np.inf
    v_max = -np.inf

    min_id = np.inf
    max_id = -np.inf

    for file_path in edges_files:
        data = pd.read_csv(file_path, sep = "\t")
        rin, suppl = process_df(data)
        v_max = max(rin["distance"].max(), v_max)
        v_min = min(rin["distance"].min(), v_min)
        min_id = min(rin["id_1"].min(), rin["id_1"].min())
        max_id = max(rin["id_2"].max(), rin["id_2"].max())

    return v_min, v_max, min_id, max_id

def make_contact_frames(folder, edges_files, output_folder, int_type, v_min, v_max, min_id, max_id):
    for file_path in edges_files:
        prot_name, num_file, _ = get_filename(folder, file_path.split("/")[-1])
        output = "{}/{}_{}.png".format(output_folder, prot_name, num_file)
        data = pd.read_csv(file_path, sep = "\t")
        rin, _ = process_df(data)
        plot_contact_map(rin, int_type, output, v_min, v_max, min_id, max_id)

print("Starting job")

if __name__ == "__main__":
    datasets = ['antibody', 'cdk6_p16ink4a', 'frataxin', 'p16', 'stim1', 'vcb', 'vhl']
    int_types = ['VDW', 'HBOND', 'PIPISTACK', 'SSBOND', 'IONIC', 'PICATION']

    c = 1
    tot = len(datasets) * len(int_types)

    for dataset in datasets:
        make_folder("output/{}".format(dataset))
        make_folder("output/{}/contacts_imgs".format(dataset))
        edge_folder = "datasets/{}/edges".format(dataset)
        edges_files = files_indexer(dataset)
        v_min, v_max, min_id, max_id = make_seq_range(edges_files)
        for int_type in int_types:
            output_folder = "output/{}/contacts_imgs/{}".format(dataset, int_type)
            make_folder(output_folder)
            make_contact_frames(dataset, edges_files, output_folder, int_type, v_min, v_max, min_id, max_id)
            print("{} % ({} - {})".format(round(c / tot * 100, 2), dataset, int_type))
            c += 1
