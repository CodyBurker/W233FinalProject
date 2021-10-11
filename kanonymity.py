# Given a list of attributes and a table
# List k-anonymity, and whether hidden attributes are still private (ranges, uniqueness based on class?)
# This might be helpful: https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/

# Dataset: https://www.kaggle.com/parulpandey/2020-it-salary-survey-for-eu-region

import pandas as pd

def read_example_dataset():
# Read example dataset
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe

# Given a dataframe and list of QIDs, return the k-Anonymity of the table
def get_k(dataset, q_identifiers):
    k = dataset.groupby(q_identifiers).size().min()
    return k

# Given a dataframe and a list of QIDs, return the equivilence classes with the the smallest K value
def smallest_classes(dataset,q_identifiers):
    equiv_class_sizes = dataset.groupby(q_identifiers).size().to_frame().reset_index()
    # Reset columns names
    col_names = q_identifiers
    col_names.append('k')
    equiv_class_sizes.columns = col_names
    # k = get_k(dataset, q_identifiers)
    return equiv_class_sizes[equiv_class_sizes.k == min(equiv_class_sizes.k)]
    
if __name__=="__main__":
    
    dataset = pd.read_csv("HW3.csv")
    # HW 3 1(c) k=31
    k = get_k(dataset, ['Sex'])
    print('K [Sex]:\t%i' % k)
    # HW 3 1(d) k=10
    k = get_k(dataset, ['Sex','Age'])
    print('K [Sex,Age]:\t%i' % k)
    # HW 3 1(e) k=2
    k = get_k(dataset, ['Sex','Age','Birth Country'])
    print('K [Sex,Age,Birth Country]:\t%i' % k)