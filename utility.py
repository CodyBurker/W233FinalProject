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

def get_KL(p,q):
    """
    calculate Kullbacl-Leibler divergence between original discrete probability
    p and anonymized q
    KL = sum(pi * log(pi/qi) 
    """
    if (p.shape[0] != q.shape[0]):
        KL = -1
    else
        KL = np.sum(np.where(p != 0, p * np.log(p / q), 0))
    return KL
    
    
def utility_KL(dataset0, dataset1, n):
    """
    Calculate Kullback-Leibler divergence between distributions of 
    original and generalized q_identifiers. 
    dataset0 is the original dataset
    dataset1 is the anonymized dataset
    n[i] = total number of possible records that would be anonymized to dataset1[i]
    example {sex} -> {"*"} => n = 2
    {zip code} -> remove last digit => n = 10
    {zip code} -> remove last 2 digits => n = 100 
    assumes that for all i dataset1[i] is the anonymized version of dataset1[i]
    q_identifiers0 is the original q_identifiers 
    q_identifiers1 is the anonymized q_identifiers 
    """
    # 
    [numrow numcol] = dataset0.shape
    p = 1/numrow * ones[numrow]
    ec_q = dataset1.groupby(q_identifiers1)
    for i in [0:numrow]:
        ec = equivclass of dataset0[i]
        ec_size = ec.shape[0] 
        q[i] = p[i] * ec_size * (1/n)   
    get_KL(p,q)
    return KL
    

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
    