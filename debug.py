from tomogram_datasets import all_fm_tomograms
from tomogram_datasets import all_fm_negative_tomograms

neg_tomos = all_fm_negative_tomograms()
pos_tomos = all_fm_tomograms()

for tomo in neg_tomos:
    print(tomo.filepath)