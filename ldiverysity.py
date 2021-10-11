import pandas as pd

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
   # needs implemented
   return 0

if __name__=="__main__":
    dataset = read_example_dataset()
    print(get_l_distinct(dataset, ['Age','Gender'],'Seniority level'))