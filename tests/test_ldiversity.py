import ldiversity
import pandas as pd
import pytest

# To be run with pytest
# python3 -m pytest
# or on windows something like py -m pytest

def test_get_l_distinct():
    dataset = pd.read_csv("HW3.csv")
    output = ldiversity.get_l_distinct(dataset, ['Sex'],'Drinks/Day')
    assert output == 6

def test_get_l_entropy():
    dataset = pd.read_csv("HW3.csv")
    output = ldiversity.get_l_entropy(dataset,['Sex'],'Drinks/Day')
    assert round(output,5)==round(4.2266662750043125,5)