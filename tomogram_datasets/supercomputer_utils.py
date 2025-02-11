"""
A collection of utilities for use on BYU's supercomputer.
"""


import re
import os
from .annotation import AnnotationFile
from .tomogram import TomogramFile

from typing import List, Union, Optional
import pdb
from tqdm import tqdm
import warnings
warnings.simplefilter("ignore") # Don't really need to deal with warnings right now.

def _combine_tomos(tomo1: TomogramFile, tomo2: TomogramFile) -> TomogramFile:
    """ 
    Combines two conceivably duplicate tomograms into one by merging their
    annotations. All other attributes are taken from `tomo1`, like filepath
    and such.
    """
    # Ensure that each tomogram has a list for its annotations, even if it is
    # empty
    if tomo1.annotations is None: 
        tomo1.annotations = []
    if tomo2.annotations is None: 
        tomo2.annotations = []
    # Combine annotations
    combined_annotations = tomo1.annotations + tomo2.annotations
    new_tomo = tomo1
    new_tomo.annotations = combined_annotations
    # Choose shortest filepath
    new_tomo.filepath = min(tomo1.filepath, tomo2.filepath, key=len)
    return new_tomo

def _get_label(tomo: TomogramFile) -> str:
    """ Tomogram "labels" are the filename without path nor extension. """
    return os.path.splitext(os.path.basename(tomo.filepath))[0]

class SCTomogramSet():
    """ A class to manage the tomograms we work with on the supercomputer. """
    def __init__(self):
        self.tomograms = dict()
        self.private = dict()
    def __repr__(self):
        return f'<SCTomogramSet containing {len(self.tomograms)} tomograms>'
    def append(self, new_tomogram: TomogramFile, private: bool):
        """ Add a tomogram to the set. """
        label = _get_label(new_tomogram)
        # If the tomogram isn't present, add it
        if label not in self.tomograms:
            self.tomograms[label] = new_tomogram
            self.private[label] = private
        # Otherwise, combine its annotations with the existing tomogram's
        # annotations. 
        else:
            self.tomograms[label] = _combine_tomos(self.tomograms[label], new_tomogram)
            # If two matching tomograms have different privacy, make them both public
            if self.private[label] != private:
                self.private[label] = False

    def get_all_tomograms(self) -> List[TomogramFile]:
        """ Get all of the supercomputer tomograms. """
        return self.tomogram.values()
    def get_private_tomograms(self) -> List[TomogramFile]:
        """ Get all of the private (test) supercomputer tomograms. """
        requested_tomograms = []
        for label in self.tomograms:
            if self.private[label]:
                requested_tomograms.append(self.tomograms[label])
        return requested_tomograms
    def get_public_tomograms(self) -> List[TomogramFile]:
        """ Get all of the public (train) supercomputer tomograms. """
        requested_tomograms = []
        for label in self.tomograms:
            if not self.private[label]:
                requested_tomograms.append(self.tomograms[label])
        return requested_tomograms

def get_fm_tomogram_set() -> SCTomogramSet:
    """
    Collect all tomograms that have been reviewed for flagellar motors from
    BYU's supercomputer into an SCTomogramSet. 
    
    From an SCTomogramSet `tomo_set`, get public tomograms with
    `tomo_set.get_public_tomograms()`.

    Does not initially load the tomogram image data. Given a `Tomogram` called
    `tomo`, one can load and access the image data in one step with
    `tomo.get_data()`.

    Returns:
        SCTomogramSet containing annotated tomograms
    """
    # Collect all tomograms together into an SCTomogramSet.
    tomogram_set = SCTomogramSet()

    tomograms = [] # A temporary list to collect tomograms. To be placed into the tomogram_set later.

    ### PUBLIC POSITIVES ###
    print(f'\nLoading public positives.\n\tCurrent number of tomograms: {len(tomogram_set.tomograms)}\n')
    # ~~~ DRIVE 1 ~~~ #
    # Hylemonella
    root = f"/grphome/grp_tomo_db1_d1/nobackup/archive/TomoDB1_d1/FlagellarMotor_P1/Hylemonella gracilis"
    dir_regex = re.compile(r"yc\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^fm.mod$", re.IGNORECASE)
    tomogram_regex = re.compile(r".*\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # ~~~ DRIVE 2 ~~~ #
    # Legionella
    root = f"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/legionella"
    dir_regex = re.compile(r"dg\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # Pseudomonas
    root = f"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Pseudomonasaeruginosa/done"
    dir_regex = re.compile(r"ab\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # Proteus_mirabilis
    root = f"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Proteus_mirabilis"
    dir_regex = re.compile(r"qya\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM\.mod$")
    tomogram_regex = re.compile(r".*\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # ~~~ DRIVE 3 ~~~ #
    # Bdellovibrio
    root = f"/grphome/grp_tomo_db1_d3/nobackup/archive/TomoDB1_d3/jhome_extra/Bdellovibrio_YW"
    dir_regex = re.compile(r"yc\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^flagellum_SIRT_1k\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # Azospirillum
    root = f"/grphome/grp_tomo_db1_d3/nobackup/archive/TomoDB1_d3/jhome_extra/AzospirillumBrasilense/done"
    dir_regex = re.compile(r"ab\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM3\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # Add tomograms to `tomogram_set` and reset the temporary collection list `tomograms`
    for tomo in tomograms:
        tomogram_set.append(tomo, private=False)
    tomograms = []
    
    print(f'Loading private positives.\n\tCurrent number of tomograms: {len(tomogram_set.tomograms)}\n')
    ### PRIVATE POSITIVES ###
    # ~~~ ZHIPING ~~~ #
    root = f"/grphome/fslg_imagseg/nobackup/archive/zhiping_data/caulo_WT/"
    dir_regex = re.compile(r"rrb\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^flagellum\.mod$")
    tomogram_regex = re.compile(r".*\.rec$")
    
    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms
    
    # ~~~ ANNOTATION PARTY ~~~ #
    root = f"/grphome/grp_tomo_db1_d4/nobackup/archive/ExperimentRuns/"
    dir_regex = re.compile(r"(sma\d{4}.*)|(Vibrio.*)")
    directories = seek_dirs(root, dir_regex)

    flagellum_regex = re.compile(r"flagellar_motor\.mod")
    tomogram_regex = re.compile(r".*\.mrc$")

    these_tomograms = seek_annotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex], 
        ["Flagellar Motor"]
    )
    tomograms += these_tomograms

    # Add tomograms to `tomogram_set` and reset the temporary collection list `tomograms`
    for tomo in tomograms:
        tomogram_set.append(tomo, private=True)
    tomograms = []

    print(f'Loading public negatives.\n\tCurrent number of tomograms: {len(tomogram_set.tomograms)}\n')
    ### PUBLIC NEGATIVES ###
    # ~~~ DRIVE 1 ~~~ #
    # Hylemonella
    root = f"/grphome/grp_tomo_db1_d1/nobackup/archive/TomoDB1_d1/FlagellarMotor_P1/Hylemonella gracilis"
    dir_regex = re.compile(r"yc\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^fm.mod$", re.IGNORECASE)
    tomogram_regex = re.compile(r".*\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # ~~~ DRIVE 2 ~~~ #
    # Legionella
    root = f"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/legionella"
    dir_regex = re.compile(r"dg\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # Pseudomonas
    root = f"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Pseudomonasaeruginosa/done"
    dir_regex = re.compile(r"ab\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # Proteus_mirabilis
    root = f"/grphome/grp_tomo_db1_d2/nobackup/archive/TomoDB1_d2/FlagellarMotor_P2/Proteus_mirabilis"
    dir_regex = re.compile(r"qya\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM\.mod$")
    tomogram_regex = re.compile(r".*\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # ~~~ DRIVE 3 ~~~ #
    # Bdellovibrio
    root = f"/grphome/grp_tomo_db1_d3/nobackup/archive/TomoDB1_d3/jhome_extra/Bdellovibrio_YW"
    dir_regex = re.compile(r"yc\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^flagellum_SIRT_1k\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # Azospirillum
    root = f"/grphome/grp_tomo_db1_d3/nobackup/archive/TomoDB1_d3/jhome_extra/AzospirillumBrasilense/done"
    dir_regex = re.compile(r"ab\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^FM3\.mod$")
    tomogram_regex = re.compile(r".*SIRT_1k\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # Add tomograms to `tomogram_set` and reset the temporary collection list `tomograms`
    for tomo in tomograms:
        tomogram_set.append(tomo, private=False)
    tomograms = []

    # ~~~ NEGATIVES BRAXTON FOUND ON RANDY DATA ~~~ #
    root = f"/grphome/grp_tomo_db1_d3/nobackup/autodelete/negative_data"
    these_tomograms = [TomogramFile(os.path.join(root, path), load=False) for path in os.listdir(root)]
    tomograms += these_tomograms

    print(f'Loading private negatives.\n\tCurrent number of tomograms: {len(tomogram_set.tomograms)}\n')
    ### PRIVATE NEGATIVES ###
    # ~~~ ZHIPING ~~~ #
    root = f"/grphome/fslg_imagseg/nobackup/archive/zhiping_data/caulo_WT/"
    dir_regex = re.compile(r"rrb\d{4}.*")
    directories = seek_dirs(root, dir_regex)
    
    flagellum_regex = re.compile(r"^flagellum\.mod$")
    tomogram_regex = re.compile(r".*\.rec$")
    
    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms

    # ~~~ ANNOTATION PARTY ~~~ #
    root = f"/grphome/grp_tomo_db1_d4/nobackup/archive/ExperimentRuns/"
    dir_regex = re.compile(r"(sma\d{4}.*)|(Vibrio.*)")
    directories = seek_dirs(root, dir_regex)

    flagellum_regex = re.compile(r"flagellar_motor\.mod")
    tomogram_regex = re.compile(r".*\.mrc$")

    these_tomograms = seek_unannotated_tomos(
        directories, 
        tomogram_regex, 
        [flagellum_regex]
    )
    tomograms += these_tomograms 

    # Add tomograms to `tomogram_set` and reset the temporary collection list `tomograms`
    for tomo in tomograms:
        tomogram_set.append(tomo, private=True)
    tomograms = []   

    print(f'Loading complete.\n\tCurrent number of tomograms: {len(tomogram_set.tomograms)}\n')

    # Return the completed set
    return tomogram_set


def seek_file(directory: str, regex: re.Pattern) -> Union[str, None]:
    """Search for a file matching the given regex recursively in the specified
    directory.

    Args:
        directory (str): The root directory to start the search. 
        regex (re.Pattern): The regex pattern to match the filenames.

    Returns:
        The full path of the matching file, or None if no match is found.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if regex.match(file):
                return os.path.join(root, file)
        for dir in dirs:
            target = seek_file(dir, regex)
            if target is not None:
                return target
    return None

def seek_files(
        directory: str, 
        regex: re.Pattern, 
        files: Optional[List[str]] = None
    ) -> List[str]:
    """Search for all files matching the given regex recursively in the specified
    directory.

    Args:
        directory (str): The root directory to start the search. 
        
        regex (re.Pattern): The regex pattern to match the filenames.

        files (list, optional): A list to accumulate matched files. Should not be set in general usage, as this is used only for internal recursion. Defaults to None.

    Returns:
        A list of the full paths of each matching file.
    """
    if files is None:
        files = []
    for root, dirs, dir_files in os.walk(directory):
        for dir_file in dir_files:
            if regex.match(dir_file):
                files.append(os.path.join(root, dir_file))
        for dir in dirs:
            files = seek_files(os.path.join(root, dir), regex, files)
    return files

def seek_dirs(
            root: str, 
            regex: re.Pattern, 
            directories: Optional[List[str]] = None
        ) -> Union[List[str], None]:
    """Search for directories matching the given regex recursively within the
    specified root directory.

    Args:
        root (str): The root directory to start the search.

        regex (re.Pattern): The regex pattern to match the directory names.
        
        directories (list, optional): A list to accumulate matched directories. Should not be set in general usage, as this is used only for internal recursion. Defaults to None.

    Returns:
        A list of paths of matching directories.
    """
    if directories is None:
        directories = []
    for this_root, dirs, _ in os.walk(root):
        for dir in dirs:
            if regex.match(dir):
                directories.append(os.path.join(this_root, dir))
            else:
                directories = seek_dirs(dir, regex, directories)
    return directories

def seek_set(
            directory: str, 
            regexes: List[re.Pattern], 
            matches: List[str] = None
        ) -> Union[List[str], None]:
    """Recursively search the specified directory for exactly one match for each regex in the list.

    Args:
        directory (str): The directory to search.

        regexes (list of re.Pattern): A list of regex patterns to match filenames.

        matches (list, optional): A list to accumulate matches. Should not be set in general usage, as this is used only for internal recursion. Defaults to None.

    Returns:
        A list of matching file paths or None if extra matches are found.
    """
    if matches is None:
        matches = [None for _ in regexes]

    for root, dirs, files in os.walk(directory):
        for file in files:
            for r_idx, r in enumerate(regexes):
                if re.match(r, file):
                    if matches[r_idx] is None:
                        matches[r_idx] = os.path.join(root, file)
                    else:
                        return None  # Extra match found
    return matches

def seek_annotated_tomos(
            directories: List[str], 
            tomo_regex: re.Pattern, 
            annotation_regexes: List[re.Pattern], 
            annotation_names: List[str]
        ) -> List[TomogramFile]:
    """
    Collect pairs of tomogram files and their corresponding annotation files,
    without loading the tomograms. Expects one tomogram per directory.

    Args:
        directories (list of str): List of directories to search for tomograms and annotations.
        
        tomo_regex (re.Pattern): The regex pattern to match tomogram filenames.
        
        annotation_regexes (list of re.Pattern): A list of regex patterns to match annotation filenames.
        
        annotation_names (list of str): A list of names for the annotations.

    Returns:
        TomogramFile objects with their corresponding annotations.
    """
    tomos = []
    for dir in directories:
        matches = seek_set(dir, [tomo_regex] + annotation_regexes)
        if matches is not None and None not in matches:
            tomogram_file = matches[0]
            annotation_files = matches[1:]
            annotations = []
            for (file, name) in zip(annotation_files, annotation_names):
                try:
                    annotations.append(AnnotationFile(file, name))
                except Exception as e:
                    print(f"An exception occured while loading `{file}`:\n{e}\n")
            tomo = TomogramFile(tomogram_file, annotations, load=False)
            tomos.append(tomo)
    return tomos

def seek_unannotated_tomos(
            directories: List[str], 
            tomo_regex: re.Pattern, 
            annotation_regexes: List[re.Pattern], 
        ) -> List[TomogramFile]:
    """
    Collect tomogram files that don't have annotations, without loading the
    tomograms.

    Args:
        directories (list of str): List of directories to search for tomograms and annotations.
        
        tomo_regex (re.Pattern): The regex pattern to match tomogram filenames.
        
        annotation_regexes (list of re.Pattern): A list of regex patterns. If any of these patterns find a match for one of the files in a given directory in `directories`, the tomogram in that directory will not be saved and returned. 

    Returns:
        TomogramFile objects.
    """
    tomos = []
    for dir in directories:
        matches = seek_set(dir, [tomo_regex] + annotation_regexes)

        if matches is not None and None not in matches:
            # This tomogram is annotated
            continue
        else:
            # Ensure that there is a tomogram in this directory
            tomo_candidates = seek_files(dir, tomo_regex)
            n_candidates = len(tomo_candidates)
            # If there are multiple possible unannotated tomogram candidates or
            # none here, that's an issue.
            if n_candidates > 1:
                warnings.warn(f"Multiple ({n_candidates}) unannotated tomograms in {dir} found. This may mean that the regular expression used to seek tomograms is not specific enough, or that this directory is strange.")
                continue
            elif n_candidates == 0:
                warnings.warn(f"No tomograms found in {dir}.")
                continue
            # If there is one candidate, it isn't annotated.
            else:
                # Append what must be the only unannotated tomogram candidate
                tomogram_file = tomo_candidates[0]
                tomo = TomogramFile(tomogram_file, load=False)
                tomos.append(tomo) 
    return tomos