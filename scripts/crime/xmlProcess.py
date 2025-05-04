import pandas as pd
import xml.etree.ElementTree as ET

# Load and parse the XML file
tree = ET.parse('xmlData/all2024.xml')
root = tree.getroot()

# Extract data into a flat structure
data = []
for district in root.findall('District'):
    district_number = district.find('DistrictNumber').text
    for precinct in district.findall('Precinct'):
        precinct_number = precinct.find('PrecinctNumber').text
        for crime in precinct.findall('Crime'):
            crime_name = crime.find('CrimeName').text
            crime_count = int(crime.find('CrimeCount').text)
            data.append({
                'District': district_number,
                'Precinct': precinct_number,
                'CrimeName': crime_name,
                'CrimeCount': crime_count
            })

# Convert to DataFrame
df = pd.DataFrame(data)

df.to_csv('allCrime.csv', index=False)
