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

current_dir_name = os.path.dirname(__file__)
regression_base = f"{current_dir_name}/regression_tests"
plnq_script = f"{regression_base}/../../plnq.py"

def run_regression_test(name):
    print(f"Testing {name} .... ", end='')

    parts = re.findall(r"\/([^\/]+).ipynb$", name)
    basename = parts[0]

    observed_output_dir = f"{regression_base}/observed_output/{basename}"
    expected_output_dir = f"{regression_base}/expected_output/{basename}"
        
    # Specify that the uuid should be the same as the expected output (so that the directories can be identical)
    uuid = get_uuid(expected_output_dir)

    result = subprocess.run([sys.executable, plnq_script, "--destroy", "--uuid", uuid, name, observed_output_dir], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Fail with return value {result.returncode}")
        print(result.stderr)
        print(result.stdout)
    elif  are_dirs_same(expected_output_dir, observed_output_dir):
        print("Success.")
    else:
        print("Fail. Output directories differ")
       
   
if not os.path.exists(plnq_script):
    print(f"plnq_script not configured properly. {plnq_script} doesn't exist.")
    exit(1)


regression_inputs = glob.glob(f"{current_dir_name}/regression_tests/input/*.ipynb")
for test_input in regression_inputs:
    run_regression_test(test_input)



