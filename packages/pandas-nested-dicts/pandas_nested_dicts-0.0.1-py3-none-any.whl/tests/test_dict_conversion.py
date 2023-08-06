import os, json
import pandas as pd
import pytest
import pandas_nested_dicts
from pandas_nested_dicts import from_nested_dicts,to_nested_dicts


def test_from_nested_dict():
    nested_dicts = [
        {
            'a': {
                'one': {
                    'first':[0,1]
                },
                'two': [2,3]
            },
            'b': {
                'two': [4,5]
            },
            'c': [6,7]
        },
        {
            'a': {
                'one': {
                    'first':[8,9]
                },
                'two': [10,11]
            },
            'b': {
                'two': [12,13]
            },
            'c': [14,15]
        }
    ]

    df = from_nested_dicts(nested_dicts)
    assert all(
        column in df.columns for column in ['c','a.one.first', 'a.two', 'b.two']
    )
    assert len(df) == len (nested_dicts)


def test_to_nested_dicts():
    nested_dict = {
        'a': {
            'one': {
                'first':[0,1]
            },
            'two': [4,5]
        },
        'b': {
            'two': [9,1]
        },
        'c': [4,5]
    }
    df = pd.json_normalize(nested_dict)
    new_nested_dict = to_nested_dicts(df)
    assert nested_dict == new_nested_dict[0]

def test_to_nested_dicts_with_name_conflict():
    df = pd.DataFrame({
        'a': [0,1,2], # <- conflict
        'c.e': [6,7,8],
        'a.b': [3,4,5],
    })
    with pytest.raises(Exception):
        new_nested_dict = to_nested_dicts(df)


def test_DictConverter__to_nested_dicts():
    nested_dict = {
        'a': {
            'one': {
                'first':[0,1]
            },
            'two': [4,5]
        },
        'b': {
            'two': [9,1]
        },
        'c': [4,5]
    }
    df = pd.json_normalize(nested_dict)
    assert df.to_nested_dicts.dump()[0] == nested_dict


