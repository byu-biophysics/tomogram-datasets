from tomogram_datasets import seek_dirs
from tomogram_datasets import seek_annotated_tomos
from tomogram_datasets import seek_unannotated_tomos

import re

root = "/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Proteus_mirabilis"
# `dir_regex should match the target directories (directories containing a tomogram and an annotation) within `root`. Often each of these matches represents a "run".
dir_regex = re.compile(r"qya\d{4}.*") # The directories I care about all start with 'qya' and four digits
# `seek_dirs` returns a list of directories matching `dir_regex` within the provided root directory
directories = seek_dirs(root, dir_regex)

# flagellum_regex matches .mod files of the form `fm.mod`, ignoring case.
flagellum_regex = re.compile(r"^fm.mod$", re.IGNORECASE)
# tomogram_regex matches .rec files of the form `*.rec`.
tomogram_regex = re.compile(r".*\.rec$")

# Store tomograms with flagellar motor annotations in each of the directories targeted by `dir_regex` using the regexes defined above.
fm_tomograms = seek_annotated_tomos(
    directories, 
    tomogram_regex, 
    [flagellum_regex], 
    ["Flagellar Motor"]
)

# Store tomograms without flagellar motor annotations in each of the directories targeted by `dir_regex` using the regexes defined above.
no_fm_tomograms = seek_unannotated_tomos(
    directories, 
    tomogram_regex, 
    [flagellum_regex]
)

if __name__ == '__main__':
    print()