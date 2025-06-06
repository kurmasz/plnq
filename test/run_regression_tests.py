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

runner = [sys.executable, '-m', 'plnq.plnq'] # Run plnq from dev source
if len(sys.argv) > 1:
    runner = [sys.argv[1]] # Run a specific executable script.
print(f"Using {runner}")

def run_regression_test(name):

    # Remove the redundant common prefix
    prefix = os.path.commonprefix([regression_base, name])
    short_name = f".{name[len(prefix):]}"

    print(f"Testing {short_name} .... ")

    parts = re.findall(r"\/([^\/]+).ipynb$", name)
    basename = parts[0]

    observed_output_dir = f"{regression_base}/observed_output/{basename}"
    expected_output_dir = f"{regression_base}/expected_output/{basename}"
        
    # Specify that the uuid should be the same as the expected output (so that the directories can be identical)
    uuid = get_uuid(expected_output_dir)

    result = subprocess.run(runner + ["--destroy", "--uuid", uuid, name, observed_output_dir], 
                            env={**os.environ, 'PYTHONPATH': project_root},
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Fail with return value {result.returncode}")
        print(result.stderr)
        print(result.stdout)
    elif are_dirs_same(expected_output_dir, observed_output_dir):
        print("Success.")
    else:
        print("Fail. Output directories differ")
       
   
regression_inputs = glob.glob(f"{current_dir_name}/regression_tests/input/*.ipynb")
for test_input in regression_inputs:
    run_regression_test(test_input)
