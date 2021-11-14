from ldiversity import read_example_dataset
from tcloseness import get_proportions, get_t_closeness_eqv,get_t_closeness, read_example_dataset
import pandas as pd
import pytest

def test_t_closeness_prop():
    dataset = pd.read_csv("HW3.csv")
    q_identifiers = ['Sex', 'Age']
    sensitive_column = 'Drinks/Day'
    eqv_test = dataset[(dataset.Sex == 'M') & (dataset.Age == 31)]
    x = get_proportions(dataset[sensitive_column])
    prop = get_t_closeness_eqv(eqv_test, x, sensitive_column, 0)
    prop_2 = get_t_closeness_eqv(eqv_test, x, sensitive_column, 1)
    assert round(prop_2,5) == round(0.11868686868686872,5)

def test_t_closeness():
    dataset = pd.read_csv("HW3.csv")
    q_identifiers = ['Sex', 'Age']
    sensitive_column = 'Drinks/Day'
    test_1 = get_t_closeness(dataset, q_identifiers, sensitive_column, 0)
    test_1_ans = 0.09791666666666667
    assert round(test_1,5) == round(test_1_ans,5)

    test_2 = get_t_closeness(dataset, q_identifiers, sensitive_column, 1)
    test_2_ans = 0.11868686868686872
    assert round(test_2,5) == round(test_2_ans,5) 

def test_t_closeness2():
    df = pd.read_csv("IT Salary Survey EU  2020.csv")
    df['Total years of experience'] = pd.to_numeric(df['Total years of experience'], 
                                                errors = 'coerce', 
                                                downcast = 'integer').fillna(0).astype(int)
    test_1 = get_t_closeness(df, ['Age', 'City'], 'Total years of experience', 0)
    test_1_ans = 0.06055769184260804

    test_2 = get_t_closeness(df, ['Age', 'City'], 'Total years of experience', 1)
    test_2_ans = 0.9767492743264744