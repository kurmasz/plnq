
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

A template is just an `.ipynb` file. 

### First Block

The first block is a code block containing several dictionaries:

`info` contains data placed in `info.json` including: `title`, `topics`, and `tags`
```
info = {
    "title": "Writing Functions",
    "topic": "functions",
    "tags": ["functions", "hw"]
}
```


`exported_functions` is used to set up `names_from_user` in `server.py`. This shows the list of functions that the students are to write (and causes them to be exported to the automated testing.)
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

`displayed_examples` lists the input and expected output for examples that are displayed to the user.  For example
```
displayed_examples = {
    'area_of_triangle': [
        [1, 1, 1, math.sqrt(3)/4],
        [3, 4, 5, 6]
    ],
    'sum_four_digits': [
        [1111, 4],
        [1234, 10]
    ]
}
```
generates lines like this: `area_of_triangle(3, 4, 5)` should return `6`


`test_cases` lists the input and expected output for automated tests that are not shown to the students.  It has the same format as `displayed_examples`.


### Task Description Block  

After the initial metadata block, the remaining blocks describe the specific tasks. Each task requires two blocks 
  1. A Markdown block containing instructions, and 
  2. A code block containing the solution.

For the mot part, the Markdown block simply contains the text the students read. `plnq` automatically adds the sample input/output to the end of this block.

**Important:** This block should contain the function's signature somewhere delineated with `!!!`. (`plnq` uses this to build the sample input/output.)

```
# Task 1

Write a function !!!`area_of_triangle(a, b, c)`!!! That uses [Heron's Formula](https://en.wikipedia.org/wiki/Heron%27s_formula) to calculate the area of the triangle with side lengths `a`, `b`, and `c`
```




## Notes:


* To use libraries inside the description block, put the `import` statement at the top of the description block.


[^1] We originally focused on quizzes; but, didn't want to change the name when we expanded the scope to other types of assignments.