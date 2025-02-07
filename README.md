# tomogram_datasets
In the BYU Biophysics research group, 
we spend much of our time working with 3-dimensional images of bacteria called tomograms. 
Researchers have spent a lot of time looking for structures in these tomograms, and save their findings in annotation files. 
This repository contains code that makes it easier to navigate the web of tomograms and annotations we have,
simplifying analysis and dataset creation.

## Installation
Install with pip:
```shell
pip install git+https://github.com/byu-biophysics/tomogram-datasets.git
```

## Documentation
Read the documentation at [byu-biophysics.github.io/tomogram-datasets](https://byu-biophysics.github.io/tomogram-datasets/).

## Basic usage
### Basic file loading
#### Loading a tomogram


Assume a tomogram is located at `/tmp/tomogram-data/qya2015-11-19-2/atlas10003.mrc`.

Load it with
```python
path = "/tmp/tomogram-data/qya2015-11-19-12/atlas3_at20002.mrc"
tomogram = TomogramFile(path)
```

### Supercomputer Utilities
Assume a directory of directories (each of which potentially contains tomograms and annotations) is located in `/tmp/tomogram-data`. An example structure is shown below, in which some directories (the ones we really want to work with) contain a tomogram and an annotation. Others contain stuff we don't want, like "PEET_FM" below, or don't contain an annotation, like "qya2015-11-19-16". All of the directories contain at least some files we don't want.

```
/tmp/tomogram-data
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
├── qya2015-11-19-12
│   ├── atlas3_at20002.mrc            # File wanted! (tomogram)
│   ├── atlas3_at20002_part121_54.rec 
│   └── FM.mod                        # File wanted! (annotation)
├── qya2015-11-19-16                  # No .mod file, directory not wanted!
│   ├── atlas40002.mrc                # Would be wanted if it had an annotation
│   ├── atlas40002_part121_50.rec
│   └── qya2015-11-19-16.id           
├── qya2015-11-19-2
│   ├── atlas10003.mrc                # File wanted! (tomogram)
│   ├── atlas10003_part121_20.rec
│   ├── Fm.mod                        # File wanted! (annotation)
│   ├── FM.csv                        
│   └── FMinitMOTL.csv                
│   ⋮ 
│   ⋮
│   ⋮

```

Using the directory depicted above, here's one way to load all of the `.mrc` tomograms and automatically pair them with respective annotations:
```python
from tomogram_datasets import seek_dirs
from tomogram_datasets import seek_annotated_tomos

import re

root = f"/tmp/tomogram-data"
# `dir_regex should match the target directories (directories containing a tomogram and an annotation) within `root`. Often each of these matches represents a "run".
dir_regex = re.compile(r"qya\d{4}.*") # The directories I care about all start with 'qya' and four digits
# `seek_dirs` returns a list of matching directories
directories = seek_dirs(root, dir_regex)

# flagellum_regex matches .mod files of the form `fm.mod`, ignoring case.
flagellum_regex = re.compile(r"^fm.mod$", re.IGNORECASE)
# tomogram_regex matches .rec files of the form `*.rec`.
tomogram_regex = re.compile(r".*\.rec$")

# Look for tomograms in each of the directories targeted by `dir_regex` using the regexes defined above.
tomograms = seek_annotated_tomos(
    directories, 
    tomogram_regex, 
    [flagellum_regex], 
    ["Flagellar Motor"]
)
```

Note: for memory efficiency, the data in the tomograms in `tomograms` are not loaded by default. To work with the ndarray within the tomograms in `tomograms`, first call load(), i.e., for the first tomogram in the list call `tomograms[0].load()`.
