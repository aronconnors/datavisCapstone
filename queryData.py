import pandas as pd
from pandasql import sqldf

df = pd.read_csv("ridership_output.csv")

# Query string
q = "select hour_of_day, count(hour_of_day) from df group by hour_of_day"

# locals() gives pandasql access to `df`
result = sqldf(q, {'df': df})
print(result)