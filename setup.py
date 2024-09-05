from setuptools import setup, find_packages

setup(
    name='tomogram_datasets',
    version='0.1',
    packages=find_packages(),
    package_dir={'tomogram-datasets': 'tomogram_datasets'},
    install_requires=[
        'numpy',
        'scikit-image',
        'mrcfile',
        'imodmodel',
        'pandas',
        'cryoet-data-portal'
    ],
    author='Matthew Ward',
    author_email='matthew.merrill.ward@gmail.com',
    description='A package for handling tomograms and related tasks',
    url='https://github.com/byu-biophysics/tomogram-datasets/blob/master/',
)