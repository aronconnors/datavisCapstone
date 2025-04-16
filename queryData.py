import pandas as pd
from pandasql import sqldf

df = pd.read_csv("output/arrivals_output.csv")

# Query string
q = """
SELECT
    destination_station_complex_name,
    day_of_week,
    hour_of_day,
    avg(sum_estimated_average_ridership)
FROM
    df
GROUP BY
    destination_station_complex_name,
    day_of_week,
    hour_of_day
"""

# locals() gives pandasql access to `df`
result = sqldf(q, {'df': df})
print(result)

result.to_csv('output/WeekdayAverage.csv', index=False)
