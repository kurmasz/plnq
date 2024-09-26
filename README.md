
# PrairieLearn Notebook Question

`plnq` generates complete, auto-graded, notebook-based PrairieLearn questions using a specification contained in a single `.ipynb` file. Specifically, users place 
   1. the problem (i.e., function) descriptions,
   2. sample input/output,
   3. test cases, 
   4. PrairieLearn metadata, and
   5. sample solutions
   
into a single `.ipynb` file. `plnq` then uses this data to generate a complete PrairieLearn question (including `info.json`, `question.html`, `server.py`, all `workspace` files and all `test` files.) 

Using PrairieLearn terminology, `plnq` generates a single question: a directory that you would place inside `questions`. This question can have as many parts (i.e., functions to write) as you want; but, from PrairieLearn's perspective it is a single "question".

`plnq` assumes that 
  * a question is a sequence of tasks, where each task asks students to implement a well-defined function,
  * each function is tested using a set of instructor-provided tests
  * functions do not modify the input parameters. (Or, if they do, those modifications aren't tested.)

The result of running `plnq` is a complete notebook-based, auto-graded PrairieLearn question. You can modify this question (e.g., to add features not supported by `plnq`); however, be careful when doing this because running `plnq` again will overwrite these changes. (Or, if you avoid running `plnq` again, any oversights in the template will need to be fixed "by hand".)

## Usage:

Simply run `python plnq name_of_template.ipynb name/of/output/directory`.

For example, from the root of this repository, run `python plnq examples/simple_example_loop_hw.ipynb loc/of/pl/repo/questions/plnq_example`. Your chosen PrairieLearn course will now have a new question named `plnq_example`.

* The output directory is the name of the new directory that will contain the question. This should be unique for each question. (In other words, the output should be `pl-uni-cis500/questions/my_new_question` rather than `pl-uni-cis500/questions`)
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


`exported_functions` is used to set up `names_from_user` in `server.py`. This shows the list of functions that the students are to write (and causes them to be exported to the auto-grader).
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
generates lines like: `area_of_triangle(3, 4, 5) should return 6`

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

Following each Markdown block, is a code block containing the solution to each task. The purpose of the code block is to sanity-check the assignment (i.e., get the instructor to solve the problem to make sure it isn't more difficult than expected) and verify that the expected answers for the tests are correct.

### Comparing observed and expected values

By default, `plnq` simply uses `math.isclose` to compare floats and `==` to compare other values.

When comparing floats, `plnq` uses the default for `isclose` (`rel_tol=1e-9`). To specify a different tolerance, use a `FloatAnswer` for the expected value:

```
displayed_examples = {
    'final_value_monthly': [
        [100, 10, 0.05, FloatAnswer(15528.23, abs_tol=0.01)],
        [150, 15, 0.08, FloatAnswer(51905.73, abs_tol=0.01)]
    ]
}
```

`FloatAnswer` is a subclass of `Answer`.  Both are defined in `quiz_template/tests/answer.py`. In principle, different types of comparisons can be configured by creating different subclasses of `Answer` (however, I haven't had a need to do this yet, so this feature is completely untested).

# Additional Configuration

The first block of the specification can optionally contain a hash named `config`. The properties of this hash provide additional configuration options.


## Ignore Blocks

To ignore blocks (i.e., not include them in the resulting question), add a list named `ignore` to the `config` hash containing the indices of the blocks to ignore.

````
config = {
    "ignore": [3, 8] 
}
````

Note:
  1. Adding or removing blocks will change the indices of subsequent blocks and you will need to update the `ignore` list by hand.
  2. Each function requires two blocks (a Markdown description and code block with the solution). If you accidentally ignore only one of these two blocks, strange things will happen.

See `examples/ignore_blocks.ipynb`

## Pass Through Blocks

To pass a block through to the generated workspace unchanged,  add a list named `pass_through` to the `config` hash.

Note:
  1. Adding or removing blocks will change the indices of subsequent blocks and you will need to update the `pass_through` list by hand.
  2. Description blocks and the corresponding code block are generated as a pair. There is currently no way of inserting a pass-through block between the two. Also, remember that the code block in the input with the sample answer is not the same as the code block that gets inserted into the output for the students to fill out. That means that even if you put a pass-through between the description and the sample answer, the pass-through block will appear _after_ the code block.

# Notes:


* To use libraries inside the description block, put the `import` statement at the top of the description block.
* `plnq` generates `test.py`, the source code for the automated tests. That means that the test parameters and expected values need to be converted into Python literals. `plnq` uses `json.dumps` to do this. Therefore, only values that are JSON serializable are currently supported.
