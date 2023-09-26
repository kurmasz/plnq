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
import shutil
import uuid
import re

# Here is an idea:When you refer to the template files,
# Assume the template directory is in the same directory
# as this file. That way the setup can be run from anywhere.

# https://docs.python.org/3/library/argparse.html

#
# Startup / argument parsing
#

parser = argparse.ArgumentParser(prog='plnq',
                    description='Generates PrairieLearn quiz questions')
parser.add_argument('-v', '--verbose', action='store_true') 
parser.add_argument('description', metavar='filename', type=str, nargs=1,
                    help='the problem description file')
parser.add_argument('output_dir', metavar='dir_name', type=str, nargs='?',
                    help='the output directory', default='./-')
#TODO Add an optional argument --template-dir that specifies the location of the template files
# info.json, test.py, etc. 

args = parser.parse_args()

description_file_name = args.description[0]
output_dir_name = args.output_dir
template_dir_name = os.path.dirname(__file__) + "/quiz_template"

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

#TODO Make sure file exists, is a file, and is readable, or complain and quit.
print(f"Making quiz question from {description_file_name}")
print(f"Placing output in {output_dir_name}")
print(f"Template files located {template_dir_name}")

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
description_globals = {}
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
#TODO If output_dir exists, ask if the user wants to 
#  * rename/move the existing directory
#  * destroy/replace the existing directory
#  * Just put new files on top of the existing directory

if (Path(output_dir_name)).exists():
    print(f"Output path {output_dir_name} exists. Do you want to")
    print("  (Q) quit")
    print("  (D) destroy the current directory and replace it with the newly generated question")
    print("  (M) move the current directory to a backup location")

    choice = input().upper()
    if choice.startswith('Q'):
        print('Good bye')
        exit()
    elif choice.startswith('D'):
        if output_dir_name != '/':
            shutil.rmtree(output_dir_name)
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
func_name = description["exported_function"]["name"]
func_desc = description["exported_function"]["description"]

server_file = open(f"{template_dir_name}/server.py", "r")
server_file_contents = server_file.read()

f_name = description['exported_function']['name']
update1 = server_file_contents.replace('zzFUNC_NAMEzz',f_name)

f_description = description['exported_function']['description']
update2 = update1.replace('zzFUNC_DESCzz', f_description)

output_server_file = open(f"{output_dir_name}/server.py", "w")
output_server_file.write(update2)
output_question_file.close()

#
# workspace
#

Path(f"{output_dir_name}/workspace").mkdir(parents=False, exist_ok=False)
shutil.copy(f"{template_dir_name}/workspace/playspace.ipynb", f"{output_dir_name}/workspace")

lt_file = open(f"{template_dir_name}/workspace/learning_target.ipynb", "r")
learning_target = json.load(lt_file)

#TODO Verify that this is markdown

title_line = "" # ("# " + description["info"]["title"] + "\n\n")
text_block = [title_line] + description_json['cells'][1]['source']

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
method_name = possible_names[0]

if 'displayed_examples' in description and len(description['displayed_examples']) > 0:
  text_block += ["\n"]
  text_block += ["For example:\n"]
  for example in description['displayed_examples']:
      num_params = len(example) - 1
      params = json.dumps(example[:num_params])[1:-1]
      params = params.replace("true,", "True,")
      params = params.replace("false,", "False,")
      answer = example[num_params]
      text_block += [f"  * `{method_name}({params})` should return `{answer}`\n"] 


learning_target['cells'][0]['source'] = text_block

source_text =  ["#grade IMPORTANT: Do not remove or modify this line\n"]
source_text += [f'def {methods[0]}:\n']
source_text += ['    pass']

learning_target['cells'][1]['source'] = source_text

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

test_code_template_file = open(f"{template_dir_name}/tests/test.py", "r")
test_code = test_code_template_file.read()
test_code += '\n'  # Blank line in case the we loose the newline at the end of the template test.py
# test_code += f"\n  student_code_file = 'learning_target.ipynb'\n\n"

all_tests = description['displayed_examples'] + description['test_cases']


for index, test in enumerate(all_tests):
    num_params = len(test) - 1
    expected = test[num_params]
    if isinstance(expected, str):
        expected = f"'{expected}'"
    params = json.dumps(test[:num_params])

    test_code += f'  @points(1)\n'
    test_code += f'  @name("test {index + 1}")\n'
    test_code += f'  def test_{(index + 1):02d}(self):\n'  # Using a leading 0 ensures they run in numeric order 
    test_code += f"      self.verify('{f_name}', {expected}, '{params}')\n"
    test_code += '\n'

output_test_file = open(f"{output_dir_name}/tests/test.py", "w")
output_test_file.write(test_code)


#
# Verify correctness of test cases
#
# Make sure the reference solution produces the same answer as the test cases!

answer_block = description_json['cells'][2]['source']
answer_globals = {}
answer = {}
exec("".join(answer_block), answer_globals, answer)

#TODO: Check for 3rd block.
# Make sure it is a code block.
# Make sure it contains a correctly-named function.

for index, test in enumerate(all_tests):
    num_params = len(test) - 1
    given_answer = test[num_params]
    computed_answer = answer[f_name](*test[:num_params])
    if (given_answer != computed_answer):
        print(f"!!! Test {index}: Given answer {given_answer} differs from computed answer {computed_answer}")
