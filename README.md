[![Python application](https://github.com/CodyBurker/W233FinalProject/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/CodyBurker/W233FinalProject/actions/workflows/python-app.yml)
# W233 Final Project: Python Privacy Library
This library implements a variety of privacy-focused algorithms to aid in analyzing a dataset's privacy properties with python (pandas). 
Some automatically generated documentation can be found at [here](https://htmlpreview.github.io/?https://raw.githubusercontent.com/CodyBurker/W233FinalProject/main/html/index.html).
Some of the important files are:
* `kanonymity.py`: Functions to test for k-anonymity. 
* `ldiversity.py`: Functions to test for the l-diversity of a dataset. 
* `tcloseness.py`: Functions to measure t-closeness of a dataset.
* `html/`: Folder containing automatically generated HTML documentation for functions.
* `requirements.txt`: Explicit python dependencies.
* `tests/`: This folder contains unit tests (using the `pytest` framework) to check functions for consistency.
* `.github/workflows`: This folder contains a github action that runs the above tests every time a commit is made to the repo.


#Todo: 
  * [x] k-Anonymity
  * [ ] L-Diversity 
  * * [x] Distinct l-diverse
  * * [x] Entropy l-diverse
  * * [ ] Recursive (c,l)-diverse
  * [ ] t-Closeness
  * [ ] Incognito
  * [ ] Mondrian 
  * [ ] Publish to pip
