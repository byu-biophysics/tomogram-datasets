# Annotations

tomogram_datasets has two classes to represent a tomogram annotation&mdash;`Annotation` and `AnnotationFile`, which is a specific kind of annotation that comes from a file. Annotations tend to be accessed as attributes of [Tomograms](tomogram.md). The only annotations this package currently can parse from automatically from the supercomputer are flagellar motor annotations (see [Supercomputer Utilities](supercomputer_utils.md), particularly `get_fm_tomogram_set()`, which automatically pairs flagellar annotations to their respective tomograms).

See more details below.

::: tomogram_datasets.annotation