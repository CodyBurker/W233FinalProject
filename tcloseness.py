import pandas as pd
import numpy as np
import pytest

def read_example_dataset():
    """
    Read example dataset
    """
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe
    
#Requires s_attribute to be integers. If d_metric is 0, use equal ground distance. Otherwise use euclidean distance.
def get_t_closeness(dataset, q_identifiers, s_attribute, d_metric):
    #1. Need proportion of each answer from full table
    #2. Split data up into each equivalence class
    #2a. For each equivalence class, calculate the proportion of each answer
    #2b. Find the difference of the full and equivalence class proportions
    #2c. Use the formula associated with each distance metric to output t-closeness for that equivalence class
    full_prop = get_proportions(dataset[s_attribute])
    grouped = dataset.groupby(q_identifiers)
    t_list = []
    for name, group in grouped:
        t_list.append([name, get_t_closeness_eqv(group, full_prop, s_attribute, d_metric)])
    t_list = pd.DataFrame(t_list)
    return max(pd.DataFrame(t_list)[1])
    

# Dataset to compare, full proportions, sensitive attribute, distance metric
def get_t_closeness_eqv(dataset, full, s_att, d_metric):
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
    s_counts = s.value_counts()
    s_counts = s_counts.sort_index()
    return s_counts/sum(s_counts)

if __name__=="__main__":
    dataset = pd.read_csv("HW3.csv")
    
    print(get_t_closeness(dataset, ['Sex'],'Drinks/Day', 0))
    print(get_t_closeness(dataset,['Sex'],'Drinks/Day', 1))