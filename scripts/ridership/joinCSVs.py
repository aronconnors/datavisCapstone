import pandas as pd

###this was how we aggregated the two datasets since we weren't allowed to do it on the NYS API

df1 = pd.read_csv('arrivalsWeekdayAvg.csv', header=None)
df2 = pd.read_csv('departuresWeekdayAvg.csv', header=None)

df1.columns = ['station', 'day', 'hour', 'riders']
df2.columns = ['station', 'day', 'hour', 'riders']

combined = pd.concat([df1, df2])
combined['riders'] = pd.to_numeric(combined['riders'], errors='coerce')

grouped = combined.groupby(['station', 'day', 'hour'], as_index=False)['riders'].sum()

grouped.to_csv('stationBusiness.csv', index=False)

print(grouped)
