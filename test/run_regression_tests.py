###############################################################################
#
# run_regression_tests.py
#
# run the plnq regression tests
#
# (c) 2024 Zachary Kurmas
#
###############################################################################

import glob
import os
import sys
import re
import subprocess
import filecmp
import json

##############################################################################
#
# Directory comparisons
#
##############################################################################


# From https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi
class dircmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """
    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files,
                                 shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp


# From https://stackoverflow.com/questions/4187564/recursively-compare-two-directories-to-ensure-they-have-the-same-files-and-subdi
def are_dirs_same(dir1, dir2):
    """
    Compare two directory trees content.
    Return False if they differ, True is they are the same.
    """
    compared = dircmp(dir1, dir2)
    if (compared.left_only or compared.right_only or compared.diff_files 
        or compared.funny_files):
        if compared.left_only:
            print("   Only in dir1:", compared.left_only)
        if compared.right_only:
            print("   Only in dir2:", compared.right_only)
        if compared.diff_files:
            print("   Differing files:", compared.diff_files)
            print(f"   diff {dir1}/{compared.diff_files[0]} {dir2}/{compared.diff_files[0]}")
        if compared.funny_files:
            print("   Non-comparable files:", compared.funny_files)
        return False
    
    for subdir in compared.common_dirs:
        if not are_dirs_same(os.path.join(dir1, subdir), os.path.join(dir2, subdir)):
            return False
    return True

def get_uuid(assignment_directory):
    if not os.path.exists(assignment_directory):
        raise FileNotFoundError(f"Expected output directory '{assignment_directory}' does not exist.")
    with open(f"{assignment_directory}/info.json") as file:
        data = json.load(file)
        return data['uuid']

##############################################################################
#
# main
#
##############################################################################

# Get the absolute path to the project root (1 level up from this file)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

current_dir_name = os.path.dirname(__file__)
regression_base = os.path.join(current_dir_name, "regression_tests")
observed_output_base = os.path.join(regression_base, 'observed_output')

# Create the directory if it doesn't exist
if not os.path.exists(observed_output_base):
    os.makedirs(observed_output_base)    

runner = [sys.executable, '-m', 'plnq'] # Run plnq from dev source
if len(sys.argv) > 1:
    runner = [sys.argv[1]] # Run a specific executable script.
print(f"Using {runner}")

from pathlib import Path
from typing import Union


def handle_symlink_in_windows(filepath: Union[str, Path]) -> bool:
    """
    Return symlink "target" iff *filepath* is a text file that

    1. contains **exactly one non-empty line** (ignoring a trailing newline),
    2. whose contents, after trimming surrounding whitespace, form a
       valid path to a file, and
    3. that target file **exists and is readable** by the current process.

    Parameters
    ----------
    filepath : str | pathlib.Path
        Path to the file you want to inspect.
    """
    p = Path(filepath)
    if p.is_dir():
        return filepath

    # Must exist, be a regular file, and be readable.
    if not (p.is_file() and os.access(p, os.R_OK)):
        raise ValueError(f"Parameter {filepath} is not a readable, regular file.")

    # Read the file *once* without loading more than one line.
    with p.open("r", encoding="utf‑8", errors="replace") as f:
        first_line = f.readline()
        remainder   = f.readline()  # Empty string only if no second line

    # Reject if there are zero or >1 lines (non‑empty remainder)
    # or if the lone line is just whitespace.
    candidate = first_line.rstrip("\n\r")
    if not candidate.strip() or remainder:
        return filepath

    target = (Path(filepath).resolve().parent / candidate).resolve()

    # Must be an existing readable file (not dir, symlink is OK).
    if (target.is_file() or target.is_dir()) and os.access(target, os.R_OK):
        return target
    else:
        return filepath


def run_regression_test(name):

    print(f"Old Name: {name}")
    name = handle_symlink_in_windows(name)
    print(f"New Name: {name}")


    filename, basename = (p := Path(name)).name, p.stem
    print(f"{filename} --- {basename}")

    print(f"Testing {filename} .... ", end='')

    observed_output_dir = f"{regression_base}/observed_output/{basename}"
    expected_output_dir = f"{regression_base}/expected_output/{basename}"
        
    # Specify that the uuid should be the same as the expected output (so that the directories can be identical)
    uuid = get_uuid(expected_output_dir)

    result = subprocess.run(runner + ["--destroy", "--uuid", uuid, name, observed_output_dir], 
                            env={**os.environ, 'PYTHONPATH': project_root},
                            capture_output=True, text=True)
    print(result.stderr)
    if result.returncode != 0:
        print(f"\nFail with return value {result.returncode}")
        print(result.stderr)
        print(result.stdout)
    elif are_dirs_same(expected_output_dir, observed_output_dir):
        print("Success.")
    else:
        print("Fail. Output directories differ")
       
   
regression_inputs = glob.glob(f"{current_dir_name}/regression_tests/input/*.ipynb")
regression_inputs.append(f"{current_dir_name}/regression_tests/input/workspace_with_data_files")
for test_input in regression_inputs:
    run_regression_test(test_input)
