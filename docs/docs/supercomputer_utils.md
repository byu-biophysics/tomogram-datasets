# Supercomputer Utilities

The functions described here tend to be useful when navigating the labyrinth that is our supercomputer to find tomograms and (for now) their associated flagellar motor annotations. `get_fm_tomogram_set` is particularly useful. It parses the supercomputer for the tomograms and annotations that essentially make up the dataset for the Kaggle competition we are launching.

They are each imported directly to `tomogram_datasets`; in other words, to import `get_fm_tomogram_set`, one may simply call `from tomogram_datasets import get_fm_tomogram_set`.

## Parsing the supercomputer for tomograms with/without annotations
The supercomputer directory `"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Proteus_mirabilis"` contains a number of tomograms, some of which have flagellar motor annotations, and some of which do not. The general structure is shown below. 

```
/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Proteus_mirabilis
├── PEET_FM                           # Unwanted directory
│   ├── Run10
│   │   ├── averagedFilenames.txt
│   │   ├── FM-001.log
│   │   ├── FM-002.log
│   │   ├── FM-003.log
│   │   ├── FM-004.log
│   │   ├── FM-005.log
│   │   ├── FM-006.log
│   │   ├── FM-007.log
│       ⋮
│       ⋮
│       ⋮
├── qya2015-11-19-12                  # Directory containing annotated tomogram
│   ├── atlas3_at20002.mrc            #   - Annotated tomogram
│   ├── atlas3_at20002_part121_54.rec 
│   └── FM.mod                        #   - Annotation
├── qya2015-11-19-16                  # Directory containing unannotated tomogram
│   ├── atlas40002.mrc                #   - Unannotated tomogram
│   ├── atlas40002_part121_50.rec
│   └── qya2015-11-19-16.id           
├── qya2015-11-19-2                   # Directory containing annotated tomogram
│   ├── atlas10003.mrc                #   - Annotated tomogram
│   ├── atlas10003_part121_20.rec
│   ├── Fm.mod                        #   - Annotation
│   ├── FM.csv                        
│   └── FMinitMOTL.csv                
│   ⋮ 
│   ⋮
│   ⋮

```

Say we want to find the .rec and .mod files associated with tomograms with and without flagellar motors. Some sub-directories, like `qya2015-11-19-12`, contain a .rec tomogram (`atlas3_at20002_part121_54.rec`) and an annotation (`FM.mod`. "FM" is an abbreviation for "flagellar motor"). Others don't contain an annotation, like `qya2015-11-19-16`, or they contain stuff we don't want, like "PEET_FM" below. All of the directories contain at least some files we don't want, like `qya2015-11-19-12/atlas3_at20002.mrc`. 
Here is one way to seek all `.rec` tomograms in `/grphome/grp_tomo_db1_d2/.../Proteus_mirabilis` and, if applicable, automatically pair them with respective annotations. The code uses utility functions described below on this page.

```python
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

# Store tomograms with flagellar motor annotations in each of the directories
# targeted by `dir_regex` using the regexes defined above.
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
```

After running the above code, `fm_tomograms` should contain a list of 15 [TomogramFiles](/tomogram/#tomogram_datasets.tomogram.TomogramFile), and `no_fm_tomograms` should contain a list of 5 [TomogramFiles](/tomogram/#tomogram_datasets.tomogram.TomogramFile).

::: tomogram_datasets.supercomputer_utils
