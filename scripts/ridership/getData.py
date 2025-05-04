import requests
import csv
import time

'''This is our main script to get data from the NYS open data platform. The API is really 
finicky, so a thorough wrapper like this was necessary in order to get the full dataset. 
The main constraint was you coulnd't get more than 1000 records at a time, and sometimes 
the API would just stop working instead of failing gracefully. Sometimes it would take days 
for queries returning millions of records'''

#destination origin subway dataset
#base_url = "https://data.ny.gov/resource/jsu2-fbtj.json"

#police precinct
base_url = "https://data.cityofnewyork.us/resource/y76i-bdw7.json"


#####
#SoSQL supports: [select, where, group by, having, aggregations]
#SoSQL doesn't support: [joins, subqueries, with statements, this doesnt seem to support unions either]
#####
SQL = """
SELECT *
"""

file = "output/policePrecincts.csv"

limit = 1000
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

        #best practice is to hardcode the API key just like this LMAO
        headers = {
            "X-App-Token": 'ufDxorYpothxuRuzrTA0PN9RH'
        }
        if header:
            print('getting...')
        else:
            print('getting more...')

        #only break when we get a difinitive thing that goes wrong, don't move on to the next batch until success
        while True:
            #set a timeout in the HTTP request or else it just chills and waits
            try:
                response = requests.get(base_url, params=params, headers=headers, timeout=30)
                if response.status_code == 200:
                    break
                #HTTP status 429 means too many requests. explicit API throttling
                elif response.status_code == 429:
                    print("Rate limited. Waiting 1 hour...")
                    time.sleep(3600)
                #any other HTTP status issue
                else:
                    print(f"Error {response.status_code}. Retrying in 1 minute...")
                    print(response)
                    time.sleep(60)
            #Timeout HTTP requests because this API apparrently just ignores requests based on traffic and request frequency (by IP)
            except requests.exceptions.Timeout:
                print("Timeout. Retrying in 1 minute...")
                time.sleep(60)
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}. Retrying in 1 minute...")
                time.sleep(60)
        data = response.json()
        print('got')

        #if the data is not in list form, there is something wrong with it. Otherwise its done
        if not isinstance(data, list):
            print(data)
            break
        elif not data:
            print("Done")
            break

        #increase the offset by the length of whatever is returned, not the limit
        #sometimes the API just decides to respond with less than 1000
        offset += len(data)

        #take it real slow or else they throttle tf out of us
        #TODO add random delay so that its not the same script always sending requests first if you're running more than one at a time
        time.sleep(60)


        #save output to csv file and save seperately when necessary
        #TODO shoult this writer object be outside the loop? this works ig
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        if header:
            writer.writeheader()
        writer.writerows(data)
        header = False