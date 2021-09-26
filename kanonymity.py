# Given a list of attributes and a table
# List k-anonymity, and whether hidden attributes are still private (ranges, uniqueness based on class?)
# This might be helpful: https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/

# Dataset: https://www.kaggle.com/parulpandey/2020-it-salary-survey-for-eu-region

import pandas as pd
import hashlib
import numpy as np

def read_example_dataset():
# Read example dataset
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe

def get_k(dataset, q_identifiers):
    # Generate hash to identify equivilence class (q*-block)
    k = dataset.groupby(q_identifiers).size().min()
    return k

if __name__=="__main__":
    dataset = read_example_dataset()
    k = get_k(dataset, ['Age','Gender'])
    print('K:%i' % k)