import requests
import csv
import time

base_url = "https://data.ny.gov/resource/jsu2-fbtj.json"
SQL = """
SELECT origin_station_complex_name, destination_station_complex_name, max(estimated_average_ridership)
GROUP BY origin_station_complex_name, destination_station_complex_name
"""
limit = 1000
offset = 0
all_data = []

#break the query down into multiple requests to avoid the default limit
while True:
    paginated_query = f"{SQL} LIMIT {limit} OFFSET {offset}"
    params = {
        "$query": paginated_query
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    #if the data is not in list form, there is something wrong with it. Otherwise its done
    if not isinstance(data, list):
        print(data)
        break
    elif not data:
        print("Done")
        break


    all_data.extend(data)
    #increase the offset by the limit size so we can get the next piece of the response sequentially
    offset += limit

    time.sleep(0.2)

#save output to csv file and save seperately when necessary
with open("ridership_output.csv", "w", newline='', encoding='utf-8') as csvfile:
    if all_data:
        writer = csv.DictWriter(csvfile, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)