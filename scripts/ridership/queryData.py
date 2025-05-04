import pandas as pd
from pandasql import sqldf

#####
#An extremely hacky way to set up a database for easy querying of our massive datasets we got from the API
#it worked great
#####

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

result = sqldf(q, {'df': df})
print(result)

result.to_csv('output/allCrime.csv', index=False)
