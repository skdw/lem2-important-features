# lem2-important-features
Choosing important features of objects using the rough sets method. Implementation of LEM2 algorithm.

## Dataset

Data is collected from "Student alcohol consumption" [Kaggle archive](https://www.kaggle.com/uciml/student-alcohol-consumption)

### Usage
usage: process.py [--input INPUT] [--column-idx COLUMN_IDX] [--decision-lambda DECISION_LAMBDA] [--bool]

optional arguments:
  --input INPUT         data table input (default: `dataset/student-mat.csv`)
  --column-idx COLUMN_IDX
                        decision column index (default: -1)
  --decision-lambda DECISION_LAMBDA
                        decision lambda(exprert opinion) (default: `lambda df: df['G3'] > 10`)
  --bool                whether decision column contains `bool` value, otherwise `int` (default: `False`)