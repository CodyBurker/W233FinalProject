[![Python application](https://github.com/CodyBurker/W233FinalProject/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/CodyBurker/W233FinalProject/actions/workflows/python-app.yml)
# W233 Final Project: Python Privacy Library
This library implements a variety of privacy-focused algorithms to aid in analyzing a dataset's privacy properties with python (pandas). 
Some automatically generated documentation can be found at [here](https://htmlpreview.github.io/?https://raw.githubusercontent.com/CodyBurker/W233FinalProject/main/html/anonymization.html).

Some of the important files are:
* `anonymization.py`: File implementing all of the algorithms
* `html/`: Folder containing automatically generated HTML documentation for functions.
* `requirements.txt`: Explicit python dependencies.
* `tests/`: This folder contains unit tests (using the `pytest` framework) to check functions for consistency.
* `.github/workflows`: This folder contains a github action that runs the above tests every time a commit is made to the repo.