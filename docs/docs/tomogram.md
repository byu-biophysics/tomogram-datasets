# Tomograms

tomogram_datasets has two classes to represent a tomogram&mdash;`Tomogram` and `TomogramFile`, which is a specific kind of tomogram that comes from a file. One can load a tomogram from its filepath with `tomogram = tomogram_datasets.Tomogram(filepath)`, and get the tomogram's array data with `tomogram.get_data()`. Tomograms are often associated with [Annotations](annotation.md) in the `Tomogram.annotations` attribute.

See more details below.

::: tomogram_datasets.tomogram
