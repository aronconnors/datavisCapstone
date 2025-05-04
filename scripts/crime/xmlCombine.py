import pandas as pd
import xml.etree.ElementTree as ET
import os

#####
#this script simply combines the xml files into a single xml file that has all the months
#an oversight in our dataCleaning script
#####

folder_path = 'xmlData'
xml_files = ['jan2024.xml', 'feb2024.xml', 'mar2024.xml', 'apr2024.xml', 'may2024.xml', 'jun2024.xml', 'jul2024.xml', 'aug2024.xml', 'sep2024.xml', 'oct2024.xml', 'nov2024.xml', 'dec2024.xml']

combined_data = []

for file in xml_files:
    file_path = os.path.join(folder_path, file)
    tree = ET.parse(file_path)
    root = tree.getroot()
    month = file[:3].capitalize()  #extract month from filename

    for district in root.findall('District'):
        district_number = district.find('DistrictNumber').text
        for precinct in district.findall('Precinct'):
            precinct_number = precinct.find('PrecinctNumber').text
            for crime in precinct.findall('Crime'):
                crime_name = crime.find('CrimeName').text
                crime_count = crime.find('CrimeCount').text
                combined_data.append({
                    'Month': month,
                    'Precinct': precinct_number,
                    'CrimeName': crime_name,
                    'CrimeCount': crime_count
                })

df_combined = pd.DataFrame(combined_data)
df_combined.to_csv('monthlyCrime.csv', index=False)
