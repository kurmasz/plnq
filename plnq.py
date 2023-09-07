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
parser.add_argument('output_dir', metavar='dir_name', type=str, nargs=1,
                    help='the output directory')
#TODO Add an optional argument --template-dir that specifies the location of the template files
# info.json, test.py, etc. 

args = parser.parse_args()

description_file_name = args.description[0]
output_dir_name = args.output_dir[0]
template_dir_name = os.path.dirname(__file__) + "/quiz_template"

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

print("Description:")
print(description)

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

title_line = ("#" + description["info"]["title"] + "\n\n")
text_block = [title_line] + description_json['cells'][1]['source']

# find method signature and extract
#for line in text_block:
 #   /write a function `(.*)`/



#TODO !!!!! Put in the examples !!!!

learning_target['cells'][0]['source'] = text_block

source_text =  ["#grade IMPORTANT: Do not remove or modify this line\n"]
source_text += ['def the_function(a,b,c):\n']
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

test_code += f"\n    student_code_file = 'learning_target.ipynb'\n\n"

all_tests = description['displayed_examples'] + description['test_cases']

test_num = 1
for test in all_tests:
    num_params = len(test) - 1
    expected = test[num_params]
    params = json.dumps(test[:num_params])

    test_code += f'    @points(1)\n'
    test_code += f'    @name("test {test_num}")\n'
    test_code += f'    def test_{test_num}(self):\n'
    test_code += f"        self.verify('{f_name}', {expected}, '{params}')\n"
    test_code += '\n'

    test_num += 1

output_test_file = open(f"{output_dir_name}/tests/test.py", "w")
output_test_file.write(test_code)
