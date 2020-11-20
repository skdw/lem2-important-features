import pandas as pd
from lem2 import DecisionTable


def negate(function):
    def new_function(*args, **kwargs):
       return ~function(*args, **kwargs)
    return new_function


def positive_indices(series):
    return [i for i, x in enumerate(series) if x]


def lower_bound(df, decision, attributes):
    """positive decision and there are no rows 
    with the same information and negative decision
    """
    positive = decision(df)
    negative = ~positive

    def same_attributes_neg_decision(pos_row) -> pd.Series:
        """Gets a series of answers which rows are negative
        and all their attributes are the same as in the input
        """
        res = negative
        for attr in attributes:
            p = df[attr] == pos_row[attr]
            res = res & p
        return res

    def any_attrs_neg_dec_exist(i: int) -> bool:
        """Returns true if any row of index other than i-th
        has the same attributes as the i-th row
        """
        pos_row = df.iloc[i]
        s = pd.Series(x != i for x in range(len(df)))
        r = same_attributes_neg_decision(pos_row)
        return sum(s & r) == 0
    
    any_attrs = pd.Series(any_attrs_neg_dec_exist(i) for i in range(len(positive)))
    return positive & any_attrs


def upper_bound(df, decision, attributes):

    neg_dec_any_attrs_pos_dec = lower_bound(df, negate(decision), attributes)
    return ~neg_dec_any_attrs_pos_dec


def process_subset(df, keys, subset_ids) -> set:
    dt = DecisionTable(keys)
    records = df.to_dict(orient='records')
    for obj in records:
        dt.insertObject(obj)

    print("Lem2 output:")
    rules = dt.getRulesForObjects(subset_ids, verbose=True)
    return DecisionTable.extractUsedAttributes(rules, verbose=True)


def process_df(df_path, decision):
    """Processes the data and extracts attributes
    considering the subset of ids

    Args:
        df_path (str): path to the dataframe
        decision: decision function
    """
    df = pd.read_csv(df_path)
    keys = df.keys().tolist()
    print(df.head())

    # grades are not the attributes
    attributes = [k for k in keys if k.find('G')]

    lb = lower_bound(df, decision, attributes)
    ub = upper_bound(df, decision, attributes)

    # subset_ids = [1, 30, 57]
    lb_subset_ids = positive_indices(lb)
    ub_subset_ids = positive_indices(ub)

    print('\nProcessing the lower bound subset')
    lset = process_subset(df, keys, lb_subset_ids)
    print('\nProcessing the upper bound complement subset')
    uset = process_subset(df, keys, ub_subset_ids)

    lst = [lset, uset]
    union = set().union(*lst)
    return union


if __name__ == "__main__":
    df_path = 'dataset/student-mat.csv'

    def decision(df):
        """decision - is the final grade over 10?
        (can be between 0 and 20)
        """
        return df['G3'] > 10

    res = process_df(df_path, decision)
    print('\nUnion of attributes:')
    print(res)
