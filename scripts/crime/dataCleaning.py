import os
import re
import pandas as pd
import numpy as np

'''after a catastrophic failure trying to extract the crime data from nypd's PDFs, we shifted 
to extracting the data from xlsx sheets. The data is honestly written in an even less programatic 
way here, but we can use pandas for this. Using the PDF scripts as a guide for what content we 
are extracting, we made it work using the xlsx data. This script is 100% specific to the nypd's transit crime
excel sheets.'''

#extract the data from xlsx file
def extract(input_file, output_file):
    df = pd.read_excel('xlsxData/'+input_file)

    skip_substrings = ['Complaints for Offenses Described in Administrative Code 14-150(d)', 'Occuring in Transit Jurisdiction', '2024', 'Section I - Transit Jurisdiction Complaints by Transit District and Precinct']
    precinct = False
    
    with open('xmlData/'+output_file, 'w') as output_file:
        output_file.write('<Data>')
        for index, row in df.iterrows():
            col1 = str(row.iloc[0])
            col2 = str(row.iloc[1])

            #skip useless lines that appear in every sheet
            if any(sub in col1 or sub in col2 for sub in skip_substrings):
                continue
            
            if col1 == 'nan' and col2 == 'nan':
                continue

            #appears once at the bottom of each document
            if 'Grand Total' in col1:
                output_file.write('<GrandTotal>' + col2 + '</GrandTotal></Data>')
                break

            #for crime name and count
            if precinct == True:
                #check if end of precinct
                if re.match(r'^\d{3}', col1):
                    precinct = False
                else:
                    output_file.write('<Crime><CrimeName>' + col1.replace("&", "AND") + '</CrimeName><CrimeCount>' + col2 + '</CrimeCount></Crime>')
                    continue

            if 'Transit District ' in col1:
                if 'Total' in col1:
                    output_file.write('<DistrictTotal>' + col2 + '</DistrictTotal></District>')
                else:
                    output_file.write('<District><DistrictNumber>' + col1.split('Transit District ')[1] + '</DistrictNumber>')
                continue
            
            #if the first 3 characters of column 1 are digits, its a precinct entry
            if re.match(r'^\d{3}', col1):
                if 'Total' in col1:
                    output_file.write('<PrecinctTotal>' + col2 + '</PrecinctTotal></Precinct>')
                else:
                    output_file.write('<Precinct><PrecinctNumber>' + col1 + '</PrecinctNumber>')
                    precinct = True



#get all the files in the xlsx folder
files = [f for f in os.listdir('xlsxData') if os.path.isfile(os.path.join('xlsxData', f)) and not f.startswith('.')]
#files = ['all2024.xlsx']

for file in files:
    extract(file, file.replace(".xlsx", ".xml"))