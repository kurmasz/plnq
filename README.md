
# PrairieLearn Notebook Quiz

`plnq` generates complete notebook-based PrairieLearn assignments[^1] using a specification contained in a single `.ipynb` file. Specifically, users place 
   1. the problem description,
   2. sample input/output,
   3. test cases, and
   4. PrairieLearn metadata 
   
into a single `.ipynb` file, then `plnq` uses this data to generate a complete PrairieLearn question (including `info.json`, `question.html`, `server.py`, all `workspace` files and all `test` files.)

`plnq` assumes that 
  * an assignment is a sequence of tasks, where each task asks students to implement a well-defined function,
  * each function is tested using a set of instructor-provided 
  * functions do not modify the input parameters. (Or, if they do, those changes aren't tested.)

The result of running `plnq` is a complete PrairieLearn question. Users can modify this question (e.g., add parts that don't aren't 
simply auto-tested functions); however, be careful when doing this because running `plnq` again will overwrite these changes. (Or, if you avoid running `plnq` again, any oversights in the template will need to be fixed "by hand".)

## Usage:


## Notes:

* To use libraries inside of a solution, put the `import` statement _inside_ the function definition.
* To use libraries inside the description block, put the `import` statement at the top of the description block.


[^1] We originally focused on quizzes; but, didn't want to change the name when we expanded the scope to other types of assignments.