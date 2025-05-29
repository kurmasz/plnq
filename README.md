
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
  * a question is a sequence of tasks, where each task asks students to implement a well-defined function, and
  * each function is tested using a set of instructor-provided tests.

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
plnq.info = {
    "title": "Writing Functions",
    "topic": "functions",
    "tags": ["functions", "hw"]
}
```

After the initial question-level metadata block, the remaining blocks describe the specific tasks. Each task requires two blocks 
  1. A Markdown block containing instructions, and 
  2. A code block containing the solution, example input/output, test cases, and other task-level metadata.

### Task Description Block  

For the most part, the Markdown block simply contains the text the students read. `plnq` automatically adds the sample input/output to the end of this block.

**Important:** This block should contain the function's signature delineated with `!!!`. (`plnq` uses this to build the sample input/output.)

```
# Task 1

Write a function !!!`area_of_triangle(a, b, c)`!!! That uses [Heron's Formula](https://en.wikipedia.org/wiki/Heron%27s_formula) to calculate the area of the triangle with side lengths `a`, `b`, and `c`
```

### Task Code Block  

Following each Markdown block, is a code block containing the solution to each task, as well as sample input/output, test cases, and other task-level metadata. The purpose of the solution is to 
 1. sanity-check the assignment (i.e., get the instructor to solve the problem to make sure it isn't more difficult than expected) and 
 2. verify that the expected answers for the examples and tests cases are correct.

Call `plnq.add_function` to provide the additional metadata. The function takes the name of the function as the first 
parameter, followed by several named parameters:
   * `desc`: The description that appears in list of functions that students are to write. Specifically, 
   this value is used to set up `names_from_user` in `server.py`. It is also necessary so that PrairieLearn will export the function to the auto-grader.
   * `displayed_examples`: Lists the input and expected output for examples that are displayed to the user. 
   * `test_cases`: Lists the cases run when the student clicks "Save and Grade". These are not shown to the user. 
 
```
plnq.add_function('area_of_triangle', 
    desc='A function that returns the area of a triangle given the lengths of its sides',
    displayed_examples=[
        [1, 1, 1, math.sqrt(3)/4],
        [3, 4, 5, 6.0]
    ], 
    test_cases=[
        [2, 2, 2, math.sqrt(3)],
        [5, 12, 13, 30.0],
        [10, 13, 13, 60.0],
        [5, 5, 6, 12.0],
        [13, 15, math.sqrt(34), 37.5]
    ]                                
)
```

For `displayed_examples` and `test_cases` Each example/test case is a list where the first `n-1` values are parameters and the last value is the expected return value.


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

# Additional Configuration

* To ignore a Markdown block (i.e., not include it in the resulting question), add the string `!!!PLNQ.Ignore!!!` anywhere in the block. See `examples/ignore_blocks.ipynb`. By default, code blocks are not passed through to the workspace, so there is no need to explicitly ignore them.  
* To pass a Markdown block through to the generated workspace unchanged, add the string `!!!PLNQ.PassThrough!!!` anywhere in the block. See `examples/pass_through.ipynb`. The default behavior is that Markdown blocks are scanned for a function signature, and a list of example inputs and outputs is added. If a block contains neither a pass-through marker nor a function signature, `plnq` will complain.
* To pass a Code block through to the generated workspace, add a comment containing `!!!PLNQ.PassThrough!!!` anywhere in the block. This comment will not be included in the generated workspace (so don't put the pass-through marker in a comment that
that contains other content you want to keep). Note: The code that searches for the pass-through marker is not sophisticated. Don't put the pass-through marker on the same line as a literal string containing a `#`.

`plnq` searches for exact matches to the ignore and pass-through markers. If a block is not being handled properly, double-check the capitalization and the number of exclamation marks. Also, using too many exclamation marks may result in stray characters in the output.


# Dev Install

To set up for local development:
* Clone this repo
* Create a virtual python environment: `python -m venv venv`
* Activate the virtual environment: `source venv/bin/activate`
* Install this package in edit mode: `pip install -e .`

(If you don't want to use `activate`, you can run python commands out of `venv/bin`.  For example, `venv/bin/pip install -e .`)

The current minimum version is 3.9. The code uses `importlib.resources.files` which was not 
introduced until Python 3.9.

To verify whether this package will still build and run under Python 3.9
* `cd` to the project root  
* run `./docker_build`
* run `./docker_run`

This will build a Docker image with Python 3.9, then run the automated tests.

# Notes:

* To use libraries inside the description block, put the `import` statement at the top of the description block.
* `plnq` generates `test.py`, the source code for the automated tests. That means that the test parameters and expected values need to be converted into Python literals. `plnq` uses `json.dumps` to do this. Therefore, only values that are JSON serializable are currently supported.
