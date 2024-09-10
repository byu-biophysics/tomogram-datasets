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


Assume a tomogram is located at `~/Downloads/Proteus_mirabilis/qya2015-11-19-2/atlas10003.mrc`.

Load it with
```python
path = "~/Downloads/Proteus_mirabilis/qya2015-11-19-2/atlas10003.mrc"
tomogram = TomogramFile(path)
```

### Supercomputer Utilities
Assume a directory of directories (each of which contains tomograms and annotations) is located in `~/Downloads/tomogram-data`. [TODO: more detail here]


Here's one way to load all of the `.mrc` tomograms and automatically pair them with respective annotations:
```python
root = f"~/Downloads/tomogram-data"
# `dir_regex should match the target directories (directories containing a tomogram and an annotation) within `root`. Often each of these matches represents a "run".
dir_regex = re.compile(r"yc\d{4}.*")
# `seek_dirs` returns a list of matching directories
directories = seek_dirs(root, dir_regex)

# flagellum_regex matches .mod files of the form `fm.mod`.
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


