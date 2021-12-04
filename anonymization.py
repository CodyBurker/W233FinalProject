
import pandas as pd
import numpy as np
import pytest
import multiprocessing
from joblib import Parallel, delayed
from functools import partial

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

    
#Requires s_attribute to be integers. If d_metric is 0, use equal ground distance. Otherwise use euclidean distance.
def get_t_closeness(dataset, q_identifiers, s_attribute, d_metric):
    """
    Given a pandas dataframe, a list of quasi-identifiers, a sensitive attribute, and a distance metric, get the t-closeness of a dataset.
    """
    #1. Need proportion of each answer from full table
    #2. Split data up into each equivalence class
    #2a. For each equivalence class, calculate the proportion of each answer
    #2b. Find the difference of the full and equivalence class proportions
    #2c. Use the formula associated with each distance metric to output t-closeness for that equivalence class
    
    grouped = dataset.groupby(q_identifiers)
    # Get names of each equivalence class
    name_group = [(name, group) for name, group in grouped]
    # Run get_t_closeness_eqv for each group in grouped
    # In parallel to speed up computation
    # using full_prop, s_attribute, and d_metric
    full_prop = get_proportions(dataset[s_attribute])
    t_closeness_eqv = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(get_t_closeness_eqv)(group,full_prop, s_attribute, d_metric) for name, group in grouped)
    # Create t_list for each group  
    # for name, group in grouped:
    #     t_list.append([name, get_t_closeness_eqv(group, full_prop, s_attribute, d_metric)])
    # Turn names from grouped and t_list into a dataframe
    t_closeness_eqv_df = pd.DataFrame(t_closeness_eqv)
    return max(pd.DataFrame(t_closeness_eqv)[0])
    

# Dataset to compare, full proportions, sensitive attribute, distance metric
def get_t_closeness_eqv(dataset, full, s_att, d_metric):
    """
    Given a dataset to compare, the full proportions, a sensitive attribute, and a distance metric, get the t-closeness of the dataset.
    """
    s = dataset[s_att]
    eqv_prop = get_proportions(s)
    diff_prop = (full - eqv_prop).fillna(full)
    t = 0
    if d_metric == 0:
        t = sum(abs(diff_prop))/(len(diff_prop)-1)
    else:
        ind = diff_prop.index
        r_sum = 0
        r = []
        for i in range(min(ind), max(ind) + 1):
            try:
                r.append(diff_prop.loc[i])
            except KeyError:
                r.append(0)
            r_sum += abs(sum(r))
        t = r_sum/(len(r)-1)
    return t
    
        

def get_proportions(s):
    """
    Get proportions of each answer in a sensitive attribute.
    """
    s_counts = s.value_counts()
    s_counts = s_counts.sort_index()
    return s_counts/sum(s_counts)