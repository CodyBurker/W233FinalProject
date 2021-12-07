"""
Module to calculate utility measures.

"""
import pandas as pd
import numpy as np
import pytest


def read_example_dataset():
    """
    Read example dataset
    """
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe

def utility_avg(dataset, q_identifiers):
    """
    Given a dataset and an attribute, calculate utility as 
    the average size of all equivalence classes
    """                
    EC_size = dataset.groupby(q_identifiers).size()
    return average(EC_size)

def utility_discernibility(k,dataset0,dataset1,q_identifiers1):
    """
    The discernability measure
    - dataset0 is original dataset
    - dataset1 is generalized dataset BEFORE suppression
    assumes that all records in EC of size < k will be suppressed 
    - q-identifiers1 is (generalized) quasi-identifier for dataset1
    - k is k-anonymity
    """
    
    D = len(dataset0[:0]) 
    EC1 = dataset1.groupby(q_identifiers1).size()
    U = EC1 **2
    # if size of equivalence class is < k replace |E|^2 with |E|*|D|
    U.where(EC1 < k**2, EC1 * D)
    return sum(U)

def utility_norm_avg(k,dataset1,q_identifiers1):
    """
    Normalized average class size 
    (total records/ total equiv classes )/(k)
    - dataset1 is generalized dataset
    - q-identifiers1 is (generalized) quasi-identifier for dataset1
    - k is k-anonymity
    """
    
    num_rec = len(dataset1[:0]) 
    num_EC = len(dataset1.groupby(q_identifiers1))
    return (num_rec/num_EC)/k

# For two probability distributions, calculate the Earth mover's distance
def EMD(p,q, distance_metric = "equal"):
    """
    given two distributions p and q on v calculate their EMD
    assuming the values for the sensitive attribute v
    are numerical
    """
    if len(p) != len(q):
        return 0
    if distance_metric == "equal":
        return sum(abs(np.subtract(p, q))) / 2
    elif distance_metric == "ordered":
        dist = 0
        diff = np.subtract(p, q)
        for i in range(len(diff)):
            if i > 0:
                for j in range(i - 1):
                    diff[i] += diff[j]
            dist += abs(diff[i])
        return dist/(len(diff) - 1)
    return 0


if __name__=="__main__":
    
    dataset = pd.read_csv("HW3.csv")
    # Get distinct k value for q-attributes = ['Sex']
    k = EMD([0, 0.5, 1], [0.5, 0, 1])
    print(k)
    k = EMD([0, 0.5, 0.25, 0.25], [0.5, 0, 0.5, 0], "ordered")
    print(k)
    
