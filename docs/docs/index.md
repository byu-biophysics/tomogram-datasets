# tomogram_datasets

Welcome to the documentation for the `tomogram_datasets` module. This module simplifies tasks dealing with tomograms and their respective annotations. In particular, it is useful in the [BYU Biophysics Group](https://byu-biophysics.github.io/) as a tool to easily access tomograms on BYU's supercomputer (see [Supercomputer Utils](supercomputer_utils)).

## Installation
Install with pip:
```shell
pip install git+https://github.com/byu-biophysics/tomogram-datasets.git
```

## Quick Start
### Loading annotated tomograms

While in a supercomputer session, load all tomograms with their respective annotations with the following code:

```python
from tomogram_datasets import get_fm_tomogram_set

tomogram_set = get_fm_tomogram_set() # Returns an SCTomogramSet object. See "Supercomputer Utils"
train_set = tomogram_set.get_public_tomograms()  # These tomograms are publicly available. Most are also on the CryoET Data Portal
test_set = tomogram_set.get_private_tomograms()  # These tomograms are reserved for the test set on Kaggle. Sensitive data

for tomogram in train_set: # train_set is a list of TomogramFile objects. See "Tomograms"
    # Access tomogram array shape as numpy array
    tomo_shape = tomogram.shape
    # Access tomogram array data as a numpy array
    tomo_data = tomogram.get_data()
    # Access all annotation points. They're all flagellar motors, since they came from get_fm_tomogram_set()
    tomo_annotation_points = tomogram.annotation_points()
    # Access all Annotation objects attached to this tomogram.
    tomo_annotations = tomogram.annotations
```

Be aware that the first time `get_fm_tomogram_set()` is called, it may take a couple of minutes to find all of the tomograms (it tends to take no more than 30 seconds the second time). This is something that ought to be optimized in the future.

### Working with annotated tomograms in a Jupyter notebook

Paired with [visualize_voxels](https://github.com/mward19/visualize_voxels), one can analyze our tomograms within the convenience of a Python Jupyter notebook. The following code loads our public tomograms, singles out those with more than four annotation points (flagellar motors, in this case), and displays the tomogram with the annotation points plotted in the tomogram.
```python
from tomogram_datasets import get_fm_tomogram_set
from visualize_voxels import visualize

# Load tomograms
tomogram_set = get_fm_tomogram_set()
train_set = tomogram_set.get_public_tomograms()

# Find tomograms with more than four annotation points (motors)
tomograms_with_motors = [tomo for tomo in train_set if tomo.annotations is not None]
tomograms_with_many_motors = [tomo for tomo in tomograms_with_motors if len(tomo.annotation_points()) > 4]
```

```python
# Get a quick visualization the last tomogram found with more than four motors along with the motor locations
tomogram_to_visualize = tomograms_with_many_motors[-1]
motors = tomogram_to_visualize.annotation_points()

# This may take a moment, since it has to load the tomogram's array data
visualize(tomogram_to_visualize.get_data(), marks=motors)
```

```python
# One way to get a more exciting visualization
visualize(
    # TomogramFile.get_data() yields a numpy array. In get_data, set preprocess=False for faster loading but a very poor visualization
    tomogram_to_visualize.get_data(), 
    # Save as lots_of_motors.gif
    'lots_of_motors.gif',
    # Points to mark in the visualization
    marks = motors, 
    # Plot 150 of the layers in the tomogram, evenly spaced
    slices=150,
    # Display at 15 frames per second
    fps=15,
    # Set the title
    title=f'{len(motors)} flagellar motors!'
)
```

The last cell above yields the following visualization, which one can pause and move frame-by-frame interactively in a Jupyter notebook.

![10 motors](images/lots_of_motors.gif)

## Usage

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