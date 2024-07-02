#################################################################
#
# plnq --- PrairieLearn Notebook Quiz
#
# (c) 2023 Anna Carvalho and Zachary Kurmas
#
##################################################################

import argparse
import json
from pathlib import Path
import os
import uuid
import re
import sys
import shutil

from quiz_template.tests.answer import Answer, FloatAnswer, ReAnswer

# Here is an idea:When you refer to the template files,
# Assume the template directory is in the same directory
# as this file. That way the setup can be run from anywhere.

# https://docs.python.org/3/library/argparse.html

def is_directory_protected(directory):
    protected_file_path = os.path.join(directory, "do_not_overwrite") 
    return os.path.exists(protected_file_path)

# Removes an existing target directory so it can be replaced 
# by new content. However, to prevent catastrophe if the target 
# directory is mis-typed (e.g., if the parent directory is listed 
# instead of the desired target), we verify that the target directory
# doesn't contain any unexpected files.
def destroy_existing_target(directory):
    path = Path(directory)
    contents = sorted([i.name for i in list(path.iterdir())])
    if contents != ['info.json', 'question.html', 'server.py', 'tests', 'workspace']:
        print(f'Cannot destroy/overwrite {directory}')
        print('It contains files that may not have been generated by plnq.')
        print(f'If this is the correct target directory, remove it "by hand" and run plnq again.')
        exit()
    shutil.rmtree(directory)

##########################################################
#
# main
#
############################################################

#
# Startup / argument parsing
#

parser = argparse.ArgumentParser(prog='plnq',
                    description='Generates PrairieLearn quiz questions')
parser.add_argument('-v', '--verbose', action='store_true') 
parser.add_argument('--destroy', action='store_true', help='overwrite the contents of the output directory (if present)')
parser.add_argument('description', metavar='filename', type=str, nargs=1,
                    help='the problem description file')
parser.add_argument('output_dir', metavar='dir_name', type=str, nargs='?',
                    help='the output directory', default='./-')
#TODO Add an optional argument --template-dir that specifies the location of the template files
# info.json, test.py, etc. 

args = parser.parse_args()

description_loc = args.description[0]
output_dir_name = args.output_dir
template_dir_name = os.path.dirname(__file__) + "/quiz_template"

location_is_dir = os.path.isdir(description_loc)
if location_is_dir:
    files = [f for f in os.listdir(description_loc) if f.endswith('.ipynb')]
    if len(files) == 1:
        description_file_name = f'{description_loc}/{files[0]}'
    else:
        print("Location directories may only contain one .ipynb file.")
        print("(Otherwise, I don't know which file is the template file.")
        exit()
else:
    description_file_name = False

print(output_dir_name)
if output_dir_name.endswith('/-'):
    if '/' in description_file_name:
        # TODO: This should probably be replaced with a path library
        # so that it works on windows (with it's \ instead of /)
        parts = re.findall("\/([^\/]+).ipynb$", description_file_name)
        # TODO: Make sure there is a match
        basename = parts[0]
    else:
        parts = re.findall("^(.+).ipynb$", description_file_name)
         # TODO: Make sure there is a match
        basename = parts[0]
    output_dir_name = re.sub("\/-$", f'/{basename}', output_dir_name)

# Note: The --destroy flag should *not* override a do_not_overwrite file.
if is_directory_protected(output_dir_name):
    print("Cannot write to output directory because it contains a 'do_not_overwrite' file.")
    sys.exit(1)

#TODO Make sure file exists, is a file, and is readable, or complain and quit.
print(f"Making quiz question from {description_file_name}")
print(f"Placing output in {output_dir_name}")
print(f"Template files located {template_dir_name}")

other_graded_files = []
if location_is_dir:
    description_base_name = os.path.basename(description_file_name)
    other_graded_files = [f for f in os.listdir(description_loc) if f != description_base_name ]

#
# Load description
#

f = open(description_file_name, "r")
description_json = json.load(f)

#TODO: Verify that the cell_type is 'code'
#TODO: Instead of hard-coding the first cell, should we instead require a "magic line" 
# as the first line of code?

data_block = description_json['cells'][0]['source']
# print("".join(data_block))
# print("******************----------")

# Blocks run in their own namespace. We need to specifically inject
# objects into that namespace, if desired.
description_globals = {"Answer": Answer, "FloatAnswer": FloatAnswer, "ReAnswer": ReAnswer}
description = {}
exec("".join(data_block), description_globals, description)

# print("Description:")
# print(description)


##########################################################
#
# Create output
#
############################################################

#
# Create directory
#

#TODO Make sure output can be created
if args.destroy and (Path(output_dir_name)).exists() :
    destroy_existing_target(output_dir_name)
elif (Path(output_dir_name)).exists():

    print(f"Output path {output_dir_name} exists. Do you want to")
    print("  (Q) quit")
    print("  (D) destroy the current directory and replace it with the newly generated question")
    print("  (M) move the current directory to a backup location")

    choice = input().upper()
    if choice.startswith('Q'):
        print('Good bye')
        exit()
    elif choice.startswith('D'):
        destroy_existing_target(output_dir_name)
    elif choice.startswith('M'):
        print("Not implemented yet.")
        exit()
    else:
        print(f"Don't recognize option '{choice}'")
        exit()

Path(output_dir_name).mkdir(parents=False, exist_ok=False)


#
# info.json 
#

info_json_file = open(f"{template_dir_name}/info.json")
info_json = json.load(info_json_file)
info_json["uuid"] = str(uuid.uuid4())

#TODO complain if expected info is missing.
info_json['title'] = description["info"]["title"]
info_json["topic"] = description["info"]["topic"]
info_json["tags"] = description["info"]["tags"]

for file in other_graded_files:
    info_json['workspaceOptions']['gradedFiles'].append(file)

output_json_file = open(f"{output_dir_name}/info.json", "w")
json.dump(info_json, output_json_file, indent=2)
output_json_file.close()


#
# question.html
#

question_file = open(f"{template_dir_name}/question.html", "r")
question_file_contents = question_file.read()
new_question_file_contents = question_file_contents.replace('zzDESCRIPTIONzz', description["info"]["title"])

output_question_file = open(f"{output_dir_name}/question.html", "w")
output_question_file.write(new_question_file_contents)
output_question_file.close()


#
# server.py
#

server_file = open(f"{template_dir_name}/server.py", "r")
server_file_contents = server_file.read()

functions = []
for function in description['exported_functions']:
    func_name = function['name']
    func_desc = function['description']

    func_data = {
        "name": func_name,
        "description": func_desc,
        "type": "function"
    }

    functions.append(func_data)

functions_json = json.dumps(functions, indent=2)
update = server_file_contents.replace('\'zzFUNC_INFOzz\'', functions_json)

output_server_file = open(f"{output_dir_name}/server.py", "w")
output_server_file.write(update)
output_question_file.close()


#
# workspace
#

workspace_pathname = f'{output_dir_name}/workspace' 
Path(workspace_pathname).mkdir(parents=False, exist_ok=False)
shutil.copy(f"{template_dir_name}/workspace/playspace.ipynb", f"{output_dir_name}/workspace")

# If template location is a directory, copy any additional files into the workspace
for file in other_graded_files:
    shutil.copy(os.path.join(description_loc ,file), workspace_pathname)

lt_file = open(f"{template_dir_name}/workspace/learning_target.ipynb", "r")
learning_target = json.load(lt_file)

#TODO Verify that this is markdown

i = 0
for function in description['exported_functions']:
    func_name = function['name']
    title_line = "" # ("# " + description["info"]["title"] + "\n\n")
    text_block = [title_line] + description_json['cells'][i+1]['source']

    # find method signature and extract
    methods = []
    for index, line in enumerate(text_block):
        matches = re.findall("!!!`([^`]+)`!!!", line)
        methods += matches
        if (len(matches) > 0):
            text_block[index] = re.sub("!!!", "", line)

    if len(methods) > 1:
        print("ERROR: Found more than one marked method signature:", methods)
    elif len(methods) == 0:
        print("WARNING: Did not find a method signature. Using a generic 'your_function'")
        methods = ["your_function()"]

    method_signature = methods[0]
    possible_names = re.findall("^([^(]+)\(", method_signature)
    if (len(possible_names) != 1):
        print(f"ERROR: Expected exactly 1 name in {method_signature}.  Found {possible_names}")
        print("(Make sure you have a complete signature, not just a name.)")
    method_name = possible_names[0]

    if 'displayed_examples' in description and func_name in description['displayed_examples'] and len(description['displayed_examples'][func_name]) > 0:
        text_block += ["\n"]
        text_block += ["For example:\n"]
        for example in description['displayed_examples'][func_name]:
            num_params = len(example) - 1
            params = json.dumps(example[:num_params])[1:-1]
            params = params.replace("true,", "True,")
            params = params.replace("false,", "False,")
            answer = Answer.make(example[num_params])
            text_block += [f"  * `{method_name}({params})` should return `{answer.display_expected()}`\n"] 

    text_cell = {
        "cell_type": "markdown",
        "metadata": {"collapsed": False},
        "source": text_block
    }

    source_text =  ["#grade IMPORTANT: Do not remove or modify this line\n"]
    source_text += [f'def {methods[0]}:\n']
    source_text += ['    pass']

    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"collapsed": False},
        "outputs": [],
        "source": source_text
    }
    
    learning_target['cells'].extend([text_cell, code_cell])

    i += 2

output_lt_file = open(f"{output_dir_name}/workspace/learning_target.ipynb", "w")
json.dump(learning_target, output_lt_file, indent=2)
output_lt_file.close()


#
# tests
#

Path(f"{output_dir_name}/tests").mkdir(parents=False, exist_ok=False)
shutil.copy(f"{template_dir_name}/tests/ans.py", f"{output_dir_name}/tests")
shutil.copy(f"{template_dir_name}/tests/initial_code.py", f"{output_dir_name}/tests")
shutil.copy(f"{template_dir_name}/tests/setup_code.py", f"{output_dir_name}/tests")
shutil.copy(f"{template_dir_name}/tests/answer.py", f"{output_dir_name}/tests")

test_code_template_file = open(f"{template_dir_name}/tests/test.py", "r")
test_code = test_code_template_file.read()
test_code += '\n'  # Blank line in case the we loose the newline at the end of the template test.py
# test_code += f"\n  student_code_file = 'learning_target.ipynb'\n\n"

i = 0
for function in description['exported_functions']:
    func_name = function['name']
    all_tests = description['displayed_examples'][func_name] + description['test_cases'][func_name]

    for test in (all_tests):
        num_params = len(test) - 1
        expected = test[num_params]
  
        if isinstance(expected, Answer):            
            expected_str = Answer.make(expected).constructor_string()
        else:
            expected_str = Answer.value_to_literal(expected)
        params = json.dumps(test[:num_params])

        test_code += f'  @points(1)\n'
        test_code += f'  @name("test {i + 1}")\n'
        test_code += f'  def test_{(i + 1):02d}(self):\n'  # Using a leading 0 ensures they run in numeric order 
        test_code += f"      self.verify('{func_name}', {expected_str}, '{params}')\n"
        test_code += '\n'

        i += 1

output_test_file = open(f"{output_dir_name}/tests/test.py", "w")
output_test_file.write(test_code)


#
# Verify correctness of test cases
#
# Make sure the reference solution produces the same answer as the test cases!

i = 2
answer = {}
for function in description['exported_functions']:
    answer_block = description_json['cells'][i]['source']
   
    # This allows functions defined in previous answer blocks to be available in the 
    # current answer block.
    answer_globals = answer
    exec("".join(answer_block), answer_globals, answer)
    #print(f'AG: {answer}')

    #TODO: Check for 3rd block.
    # Make sure it is a code block.
    # Make sure it contains a correctly-named function.

    func_name = function['name']
    all_tests = description['displayed_examples'][func_name] + description['test_cases'][func_name]
    
    # Modify cwd to dir containing data files
    original_cwd = os.getcwd()
    description_dir = os.path.dirname(description_file_name)
    os.chdir(description_dir)

    for index, test in enumerate(all_tests):
        num_params = len(test) - 1
        given_answer = test[num_params]
        computed_answer = answer[func_name](*test[:num_params])
        
        verifier = Answer.make(given_answer)

        if (not verifier.verify(computed_answer)):
            print(f"!!! Test {index}: {verifier.message()}")

    i += 2

    # Restore original cwd
    os.chdir(original_cwd)