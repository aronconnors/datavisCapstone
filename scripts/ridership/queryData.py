import pandas as pd
from pandasql import sqldf

df = pd.read_csv("crime/allCrime.csv")

# Query string
q = """
SELECT
    Precinct,
    CrimeName,
    CrimeCount
FROM
    df
GROUP BY
    Precinct,
    CrimeName
"""

# locals() gives pandasql access to `df`
result = sqldf(q, {'df': df})
print(result)

result.to_csv('output/allCrime.csv', index=False)
