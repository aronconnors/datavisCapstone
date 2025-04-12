import requests
import csv
import time

base_url = "https://data.ny.gov/resource/jsu2-fbtj.json"
SQL = """
SELECT
    month,
    day_of_week,
    hour_of_day,
    destination_station_complex_name,
    sum(estimated_average_ridership)
GROUP BY
    destination_station_complex_name,
    month,
    day_of_week,
    hour_of_day
"""

file = "arrivals_output.csv"

limit = 999
offset = 0
all_data = []
with open(file, "w", newline='', encoding='utf-8') as csvfile:
    #break the query down into multiple requests to avoid the default limit
    header = True
    while True:
        paginated_query = f"{SQL} LIMIT {limit} OFFSET {offset}"
        params = {
            "$query": paginated_query
        }
        if header:
            print('getting...')
        else:
            print('getting more...')

        response = requests.get(base_url, params=params)
        data = response.json()
        print('got')

        #if the data is not in list form, there is something wrong with it. Otherwise its done
        if not isinstance(data, list):
            print(data)
            break
        elif not data:
            print("Done")
            break

        #increase the offset by the limit size so we can get the next piece of the response sequentially
        offset += len(data)

        time.sleep(60)


    #save output to csv file and save seperately when necessary
        
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        if header:
            writer.writeheader()
        writer.writerows(data)
        header = False