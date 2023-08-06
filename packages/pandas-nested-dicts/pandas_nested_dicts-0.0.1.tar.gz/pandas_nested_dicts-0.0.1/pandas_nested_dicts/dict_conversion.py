import pandas as pd

def list_to_nested_dict(dictionary:dict, fieldlevels:list, v:any, to_null:list=[]) -> dict:
    '''list to a nested dictionary:
        Converts: ['uno', 'due', 'tre'] to {'uno': {'due': {'tre': 4}}}
        
        Args:
            dictionary (dict): A container dictionary.
                It will be populated by the nested dictionaries.
            fieldlevels (list): A list made by of nested fields
                written as lists of field names. Ex: [ [key1, subkey11], [key2, subkey22,, subkey23],.. ]
            v (any): Value of the nested property.
        
        Returns:
            dict: a nested dict

        Example:
            dictionary = {}
            fieldlevels = ['uno', 'due', 'tre']
            v = 4
            list_to_nested_dict(d, fieldlevels, v)
            # {'uno': {'due': {'tre': 4}}}
    '''
    if type(to_null) != list:
        raise Exception(f'*to_null* must be a list of values to convert to None! It was:\n {to_null}')
    if type(dictionary) != dict:
        raise Exception(f'*d* was not a dict, it was a {type(dictionary)}: {dictionary}.' \
                f'It could be due to a names conflict. Please check whether there is any other homonym field ' \
                f'having "{dictionary}" as value.'
        )
    if len(fieldlevels) == 1:
        try:
            if v in to_null: dictionary[str(fieldlevels[0])] = None
            else: dictionary[str(fieldlevels[0])] = v
            return dictionary
        except Exception as e: print(
            f'Conversion from de-nested list to multilevel dict failed! \nd: {dictionary}\ns: {fieldslevels}\nv: {v}'
        )
    k = str(fieldlevels[0])
    if k not in dictionary.keys(): dictionary[k] = {}
    try:
        dictionary[k] = list_to_nested_dict(dictionary[k], fieldlevels[1:],v, to_null=to_null)
    except Exception as e:
        er_msg = e
        if fieldlevels[0] in dictionary:
            er_msg = f'Names conflict between a single level "{fieldlevels[0]}:{dictionary[k]}" ' \
                f' and a multilevel {fieldlevels}:{v}. They cannot exists together'
        raise Exception(f'Conversion to multilevel dictionary failed at:\n'\
            f'{fieldlevels} : {v}. \n{er_msg}')
    return dictionary

def nest_fields_from_separated_names(input_dict:dict, sep:str='.', to_null=[]) ->dict:
    ''' Creates a nested dict from a flat dict, where fields
        to be nested are written as character separated names.

        Args:
            input_dict (dict): Flat dict.
            sep (str): Separator.

        Returns:
            (dict):

        Example:
            a = {'uno_unodue': 1, 'unouno': 4, 'uno_uno_due': 7}
            sep = '_'
            nest_fields_from_separated_names(a, sep='_')
            # {'uno': {'unodue': 1, 'uno': {'due': 7}}, 'unouno': 4}
    '''
    out_dict = {}
    if all(v is None for v in input_dict.values()): return out_dict
    for k, v in input_dict.items():
        out_dict = { **out_dict, **list_to_nested_dict(out_dict, k.split(sep), v, to_null=to_null) }
    return out_dict

def to_nested_dicts(df:pd.DataFrame, sep:str='.', to_null=[], **kwargs) -> list:
    """Converts a DataFrame to a nested dicts list

        Args:
            df (pd.DataFrame): The dataframe to convert
            sep (str, optional): Separator. Defaults to '.'.

        Returns:
            list: The list of nested dicts records.

        Example:
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
            df = pd.DataFrame(nested_dict)
            df.to_nested_dicts.dump()[0]
    """
    flat_dicts_list = df.to_dict(orient='records') # list of dicts, [{}, {},..]
    dicts = []
    for mk in flat_dicts_list:
        dicts.append(nest_fields_from_separated_names(mk, sep=sep, to_null=to_null))
    return dicts

def from_nested_dicts(nested_dict:dict, **args) -> pd.DataFrame:
    """Generate a DataFrame from a nested dict

        Alias for pandas.json_normalize.

    Args:
        nested_dict (dict): The nested dict to flat into a DataFrame

    Returns:
        (pd.DataFrame): The resulting flat DataFrame
    """
    return pd.json_normalize(nested_dict, **args)

@pd.api.extensions.register_dataframe_accessor("to_nested_dicts")
class DictConverter():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def dump(self, **kwargs):
        return to_nested_dicts(self._obj, **kwargs)
