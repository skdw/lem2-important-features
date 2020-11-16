import pandas as pd
from lem2 import DecisionTable


def process_df(df_path, subset_ids):
    """Processes the data and extracts attributes
    considering the subset of ids

    Args:
        df_path (str): path to the dataframe
        subset_ids (list): list of chosen table rows IDs
    """
    df = pd.read_csv(df_path)
    keys = df.keys().tolist()
    dt = DecisionTable(keys)

    records = df.to_dict(orient='records')
    for obj in records:
        dt.insertObject(obj)

    print("Lem2 output:")
    rules = dt.getRulesForObjects(subset_ids, verbose=True)
    DecisionTable.extractUsedAttributes(rules, verbose=True)


if __name__ == "__main__":
    df_path = 'dataset/student-mat.csv'
    subset_ids = [1, 30, 57]
    process_df(df_path, subset_ids)
