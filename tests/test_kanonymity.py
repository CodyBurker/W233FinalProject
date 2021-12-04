import anonymization
import pandas as pd

def test_get_k():
    dataset = pd.read_csv("HW3.csv")
    # HW 3: 1(c)
    k = anonymization.get_k(dataset, ['Sex'])
    assert k==34
    # HW 3: 1(d)
    k = anonymization.get_k(dataset, ['Sex','Age'])
    assert k==10
    # HW 4: 1(e)
    k = anonymization.get_k(dataset, ['Sex','Age','Marital Status'])
    assert k==1
    # HW 4: 1(f)
    k = anonymization.get_k(dataset, ['Sex','Age','Birth Country'])
    assert k==2
    # HW 4: 1(g)
    k = anonymization.get_k(dataset, ['Birth Country','Race'])
    assert k==1