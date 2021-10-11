"""
Module to test for k-anonymity in the dataset.
"""

import pandas as pd
import pytest


def read_example_dataset():
    """
    Read example dataset
    """
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe
    

def get_k_table(dataset, q_identifiers):
    """
    Given a dataset and list of QIDs, return a table of 
    equivilence classes, with the number of records associated
    with each class.
    """
    k_table = dataset.groupby(q_identifiers).size().reset_index()
    k_table = k_table.rename({k_table.columns[-1]: 'KCount'}, axis=1)
    return k_table


def get_k(dataset, q_identifiers):
    """
    Given a dataframe and list of QIDs, return the k-Anonymity of the table.
    """
    k = min(get_k_table(dataset,q_identifiers)['KCount'])
    return k

def smallest_classes(dataset,q_identifiers):
    """
    Given a dataframe and a list of QIDs, return the equivilence class(es) with the the smallest k-value
    """
    k_table = get_k_table(dataset, q_identifiers)
    min_equiv_classes = k_table[k_table['KCount'] == min(k_table['KCount'])]
    return min_equiv_classes

if __name__=="__main__":
    dataset = pd.read_csv("HW3.csv")
    # Get distinct k value for q-attributes = ['Sex']
    k = get_k(dataset, ['Sex'])
    print('K [Sex]:\t%i' % k)
    # Get distinct k value for q-attributes = ['Sex','Age']
    k = get_k(dataset, ['Sex','Age'])
    print('K [Sex,Age]:\t%i' % k)
    # Get distinct k value for q-attributes = ['Sex','Age','Birth Country']
    k = get_k(dataset, ['Sex','Age','Birth Country'])
    print('K [Sex,Age,Birth Country]:\t%i' % k)