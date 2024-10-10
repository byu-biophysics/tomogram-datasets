import tomogram_datasets
from time import perf_counter as now

file_1 = "test/data/mba2011-04-12-1.mrc" # https://cryoetdataportal.czscience.com/runs/10132
    
# Load only with header
begin = now()
header_only = tomogram_datasets.TomogramFile(file_1, load=False)
time_load_header = now() - begin

# Load tomogram with its data array
begin = now()
data_and_header = tomogram_datasets.TomogramFile(file_1, load=True)
time_data_and_header = now() - begin

print(time_load_header)
print(time_data_and_header)

print(header_only.shape)
print(data_and_header.shape)