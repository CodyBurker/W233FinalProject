import pandas as pd
import numpy as np

def read_example_dataset():
# Read example dataset
    example_dataframe = pd.read_csv('IT Salary Survey EU  2020.csv')
    return example_dataframe

# Given a dataframe, quasi-identifiers, and a sensitive columns
# Return a dataframe with each equivilence classes as a row and the count of distinct sensitive
# Values for that class
def get_l_distinct(dataset, q_identifiers, sensitive_column):
    ldistinct = dataset.groupby(q_identifiers).agg({sensitive_column:"nunique"}).reset_index()
    # Rename Column
    ldistinct = ldistinct.rename({ldistinct.columns[-1]: 'LDistinct'}, axis=1)
    return ldistinct

# TODO
# Given a dataframe, quasi-identifiers, and a sensitive columns
# Return a dataframe with each equivilence class as a row and entropy
# Of each values for that class
def get_l_entropy(dataset, q_identifiers, sensitive_column):
    q_identifiers_sensitive = q_identifiers
    q_identifiers_sensitive.append(sensitive_column)
    
    # Get size of equivilence class
    equiv_class_sizes = dataset.groupby(q_identifiers[:-1]).size().to_frame().reset_index()
    # Reset columns names
    equiv_class_sizes.columns = [*equiv_class_sizes.columns[:-1], 'equiv_class_size']

    # Get count of sensitive values in each equivilence class
    sensitive_count = dataset.groupby(q_identifiers_sensitive).size().to_frame().reset_index()
    # Reset columns names
    sensitive_count.columns = [*sensitive_count.columns[:-1], 'sensitive_count']
    # Add equiv class counts back in
    sensitive_count_with_size = pd.merge(sensitive_count, equiv_class_sizes,left_on=q_identifiers[:-1], right_on=q_identifiers[:-1])
    
    sensitive_count_with_size['prob'] = sensitive_count_with_size['sensitive_count'] / sensitive_count_with_size['equiv_class_size']
    
    sensitive_count_with_size['log_prob'] = np.log(sensitive_count_with_size['prob'])
    
    sensitive_count_with_size['neg_p_log_p'] = -1 * sensitive_count_with_size['prob'] * sensitive_count_with_size['log_prob']
    
    sum_entropy = sensitive_count_with_size.groupby(q_identifiers[:-1]).agg({'neg_p_log_p':'sum'}).reset_index()
    
    sum_entropy['total_entropy'] = np.exp(sum_entropy['neg_p_log_p'])

    return sum_entropy.drop('neg_p_log_p',axis=1)

if __name__=="__main__":
    dataset = read_example_dataset()
    print(get_l_distinct(dataset, ['Age','Gender'],'Seniority level'))
    
    print(get_l_entropy(dataset,['Age','Gender'],'Seniority level'))