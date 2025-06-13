---
title: 'PLNQ: Simplifying Code Kata Preparation'
tags:
  - code kata
  - automated feedback
  - exercise sharing
authors:
  - name: Zachary Kurmas
    orcid: 0009-0002-2074-2522
    affiliation: "1"
affiliations:
  - name: Grand Valley State University
    index: 1
date: 10 April 2025
bibliography: paper.bib
---

# High-Level Description

`PLNQ` allows instructors to define small, auto-graded coding exercises (henceforth called _code katas_) using a single Jupyter notebook. In general, a code kata requires three parts:

1. A textual description of the problem to be solved
2. Test cases used by the auto-grader
3. Metadata used by the assessment environment (CodingBat, PrairieLearn, zyBooks, etc.)

A [Jupyter](https://jupyter.org/) notebook is a single document that contains both text blocks and code blocks. 
* The problem description can be placed in a text block
* Test cases can be placed in a code block
* Metadata can also be placed in a code block.

The use of a Jupyter notebook significantly simplifies the process of creating and managing code katas as compared to other kata platforms which typically either (a) place each component in a separate file, or (b) require users to enter all the components into a single file or web form that only supports one type of formatting.  

The current version of PLNQ supports the preparation of Python exercises for [PrairieLearn](https://www.prairielearn.com/); however, 
* It would not be difficult to add support for other platforms such as [CodingBat](https://codingbat.com/), [Donda](https://dodona.be/), etc.
* Adding support for additional programming languages is trivial for languages Jupyter supports directly. Adding support for other languages is possible, but might not be practical.

The `PLNQ` source is available on GitHub (<https://github.com/kurmasz/plnq>) and is licensed under the [GNU GPL v3](https://opensource.org/license/gpl-3-0). In addition, `PLNQ` is available as a PyPi package: [plnq-gvsu](https://pypi.org/project/plnq-gvsu/). 

The GitHub repository contains both
* A set of [examples](https://github.com/kurmasz/plnq/tree/main/examples) illustrating each major feature, and
* [Complete documentation](https://github.com/kurmasz/plnq/blob/main/README.md).

In addition, 
* I have shared the PrairieLearn assignment I created using `PLNQ` for my Python course. You can browse them [here](https://us.prairielearn.com/pl/public/course_instance/184291/assessments).
* You can also watch a [video](https://youtu.be/avWnrxCU6C0?si=HD41qngdzYdxBVhS) that explains my motivation for creating `PLNQ`, then walks through the different components of a template notebook as well as the execution of `PLNQ` to produce a working PrairieLearn question.

## Statement of Need:

Writing code is a skill that requires significant practice [@spacco:2015]. One popular method of practice is to complete many _code katas_: short, focused coding exercises --- preferably in an environment that provides immediate feedback[@edwards:2019]. There are many platforms[^1] that provide this type of practice; however, preparing katas presents some logistical challenges. 

A typical kata requires, at minimum
* a problem description
* a set of test cases, and 
* some metadata.

Each of these components is best edited and managed using a different format.
* The problem description is often a plain text file, HTML, Markdown, or Latex.
* The set of test cases is often source code (although it could also be a data serialization format like `json`, `yaml`, or `XML`).
* The metadata is often a data serialization format (although it could also be source code).

The use of different formats leads to a tension between ease of preparation/editing, and ease of management: It is easiest enter a code kata when each component is placed in a separate file where authors can use different support tools (syntax highlighters, formatters, linters etc.). However, it is easiest to manage and distribute a code kata when the entire kata is contained in a single file. Placing the entire kata in a single file can also simplify editing by reducing the need to switch between tabs/files. 

The large number of code kata platforms demonstrates that either approach can work; however, the fact that there is such a large number of platforms suggests that many users aren't completely satisfied with currently available options. 

In addition, because different platforms take different approaches to managing katas, it is difficult for instructors at different institutions to share katas unless they happen to use the same platform. (Sharing is especially difficult in the case when the platforms use differing sets of files.) 

`PLNQ` provides the best of both options by using a single Jupyter notebook to define a code kata. Jupyter notebooks contain both text and code blocks, allowing authors to place all of a kata's components into a single file, yet still manage each component using the most appropriate highlighting and formatting tools. Jupyter notebook platforms provide text-focused highlighting and formatting tools for text blocks, as well as code-focused syntax highlighting and formatting tools for code blocks.  





[^1]: Just a few of the many platforms that provide code katas: [CodingBat](https://codingbat.com/), [CloudCoder](https://cloudcoder.org/), [CodeWorkout](https://codeworkout.cs.vt.edu/), [Donda](https://dodona.be/), [zyBooks](https://www.zybooks.com/).


