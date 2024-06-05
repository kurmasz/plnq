
# PrairieLearn Notebook Quiz

`plnq` generates complete notebook-based PrairieLearn assignments[^1] using a specification contained in a single `.ipynb` file. Specifically, users place 
   1. the problem description,
   2. sample input/output,
   3. test cases, and
   4. PrairieLearn metadata 
   
into a single `.ipynb` file. `plnq` then uses this data to generate a complete PrairieLearn question (including `info.json`, `question.html`, `server.py`, all `workspace` files and all `test` files.)

`plnq` assumes that 
  * an assignment is a sequence of tasks, where each task asks students to implement a well-defined function,
  * each function is tested using a set of instructor-provided tests
  * functions do not modify the input parameters. (Or, if they do, those modifications aren't tested.)

The result of running `plnq` is a complete PrairieLearn question. Users can modify this question (e.g., add parts that aren't 
simply auto-tested functions); however, be careful when doing this because running `plnq` again will overwrite these changes. (Or, if you avoid running `plnq` again, any oversights in the template will need to be fixed "by hand".)

## Usage:

Simply run `plnq name_of_template.ipynb name/of/output/directory`.

The output directory is the name of the directory into which the assignment will be placed. This should be unique for each assignment. (In other words, the output should be `pl-uni-cis500/questions/my_new_question` rather than `pl-uni-cis500`)

* The output directory is optional and defaults to the name of the template without the `.ipynb` extension.
* `plnq` is very paranoid about overwriting directories. That's by design. (I have nightmares about accidentally doing something dumb like `plnq new_question.ipynb ~`.)

## Template configuration

A template is just an `.ipynb` file. The first block is a code block containing several dictionaries:

* `info` contains data placed in `info.json` including: `title`, `topics`, and `tags`

```
info = {
    "title": "Writing Functions",
    "topic": "functions",
    "tags": ["functions", "hw"]
}
```


* `exported_functions` is used to set up `names_from_user` in `server.py`. This shows the list of functions that the students are to write (and causes them to be exported to the automated testing.)

```
exported_functions = [
    {
        'name': 'area_of_triangle',
        'description': "A function that returns the area of a triangle given the lengths of its sides"
    },
    {
        'name': 'sum_four_digits',
        'description': "A function that returns the sum of the digits in a four-digit number"
    }
]
```


## Notes:


* To use libraries inside the description block, put the `import` statement at the top of the description block.


[^1] We originally focused on quizzes; but, didn't want to change the name when we expanded the scope to other types of assignments.