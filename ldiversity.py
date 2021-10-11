"""
Module to test for various l-diversity metrics within a dataset.
"""
import pandas as pd
import numpy as np
import pytest


def read_example_dataset():
    '''
    Read example dataset
    '''
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe


def get_l_distinct_table(dataset, q_identifiers, sensitive_column):
    '''
    Given a dataframe, quasi-identifiers, and a sensitive column
    Return a dataframe with each equivilence classes as a row and the count of distinct sensitive
    Values for that class
    '''
    ldistinct = dataset.groupby(q_identifiers).agg({sensitive_column:"nunique"}).reset_index()
    # Rename Column
    ldistinct = ldistinct.rename({ldistinct.columns[-1]: 'LDistinct'}, axis=1)
    return ldistinct


def get_l_distinct(dataset, q_identifiers, sensitive_column):
    """
    Given a dataframe, a list of quasi-identifiers, and a sentive column, return
    the largest l value that the table is l-distinct for.
    """
    l_distinct_table = get_l_distinct_table(dataset, q_identifiers, sensitive_column)
    return min(l_distinct_table['LDistinct'])


def get_l_entropy_table(dataset, q_identifiers, sensitive_column):
    """
    Given a dataframe, quasi-identifiers, and a sensitive columns
    Return a dataframe with each equivilence class as a row and entropy
    Of sensitive values for that class
    """
    q_identifiers_sensitive = q_identifiers
    q_identifiers_sensitive.append(sensitive_column)
    equiv_class_sizes = dataset.groupby(q_identifiers[:-1]).size().to_frame().reset_index()
    equiv_class_sizes.columns = [*equiv_class_sizes.columns[:-1], 'equiv_class_size']
    sensitive_count = dataset.groupby(q_identifiers_sensitive).size().to_frame().reset_index()
    sensitive_count.columns = [*sensitive_count.columns[:-1], 'sensitive_count']
    sensitive_count_with_size = pd.merge(sensitive_count, equiv_class_sizes,left_on=q_identifiers[:-1], right_on=q_identifiers[:-1])
    sensitive_count_with_size['prob'] = sensitive_count_with_size['sensitive_count'] / sensitive_count_with_size['equiv_class_size']
    sensitive_count_with_size['log_prob'] = np.log(sensitive_count_with_size['prob'])
    sensitive_count_with_size['neg_p_log_p'] = -1 * sensitive_count_with_size['prob'] * sensitive_count_with_size['log_prob']
    sum_entropy = sensitive_count_with_size.groupby(q_identifiers[:-1]).agg({'neg_p_log_p':'sum'}).reset_index()
    sum_entropy['total_entropy'] = np.exp(sum_entropy['neg_p_log_p'])
    return sum_entropy.drop('neg_p_log_p',axis=1)

def get_l_entropy(dataset, q_identifiers, sensitive_column):
    """
    Get entropy l-diversity for entire dataset
    """
    entropy_table = get_l_entropy_table(dataset, q_identifiers, sensitive_column)
    return min(entropy_table['total_entropy'])

if __name__=="__main__":
    dataset = pd.read_csv("HW3.csv")
    
    # HW 3 4(a)
    print(get_l_distinct(dataset, ['Sex'],'Drinks/Day')) # Expected: 6
    print(get_l_entropy(dataset,['Sex'],'Drinks/Day'))# Expected: 4.22