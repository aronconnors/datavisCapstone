import fitz
import os
import re

'''we initially thought that the data in the PDF was easier to read and parse through programatically. 
We extracted the HTML out of these PDFs released by the NYPD and were able to use the indentation values 
and other metadata in the HTML to extract semi-structured data. This actually worked beautifully, however,
SEPTEMBER HAS INCONSISTANT INDENTATION, ITS THE ONLY ONE THAT HAS THIS, AND IT RUINED OUR WHOLE DATASET!

Got to switch to using the xlsx data, even though it is written out for humans to read it, it is not structured
data at all'''

#output an html extraction of the pdf to /directory/file.html
def pdf_to_html(pdf_path, html_output_path):
    pdf_document = fitz.open(pdf_path)
    html_content = "<html><body>"
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        html_content += page.get_text("html")
    html_content += "</body></html>"
    with open(html_output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    pdf_document.close()

#create a txt file of the actual html code in /directory to be used in the data extraction
def html_to_text(html_path, text_output_path):
    with open(html_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    with open(text_output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(html_content)

#extract the data from htmlText file
def extract(file, destination):
    district = False
    grandTotal = False
    districtTotal = False
    precinctTotal = False

    skip_substrings = ['id="page0"', '</div>', 'left:302.8pt', 'left:52.8pt', 'left:299.9pt', 'left:80.7pt', 'left:166.6pt', 'left:192.6pt', 'left:328.3pt', 'left:206.0pt', 'left:200.3pt', 'left:206.8pt']
    
    with open(file, 'r') as input_file:
        with open('xmlData/'+destination, 'w') as output_file:
            output_file.write('<Data>')
            for line in input_file:
                if any(sub in line for sub in skip_substrings):
                    continue
                elif precinctTotal == True:
                    output_file.write('<PrecinctTotal>' + re.sub(r'<.*?>', '', line.strip()) + '</PrecinctTotal></Precinct>')
                    precinctTotal = False
                    continue
                elif districtTotal == True:
                    output_file.write('<DistrictTotal>' + re.sub(r'<.*?>', '', line.strip()) + '</DistrictTotal></District>')
                    districtTotal = False
                    continue
                elif grandTotal == True:
                    output_file.write('<MonthTotal>' + re.sub(r'<.*?>', '', line.strip()) + '</MonthTotal></Data>')
                    break
                else:
                    if 'left:53.1pt' in line:
                        if district == False:
                            if 'Grand Total' in line:
                                grandTotal = True
                            else:
                                district = True
                                output_file.write('<District><DistrictNumber>' + re.sub(r'<.*?>', '', line.strip()) + '</DistrictNumber>')
                        else:
                            district = False
                            districtTotal = True
                            continue
                    elif 'left:60.6pt' in line:
                        if 'Total' in line:
                            precinctTotal = True
                        else:
                            output_file.write('<Precinct><PrecinctNumber>' + re.sub(r'<.*?>', '', line.strip()) + '</PrecinctNumber>')
                    elif 'left:67.9pt' in line:
                        output_file.write('<Crime><CrimeName>' + re.sub(r'<.*?>', '', line.strip()) + '</CrimeName>')
                    elif 'left:353.5pt' in line or 'left:350.7pt':
                        output_file.write('<CrimeCount>' + re.sub(r'<.*?>', '', line.strip()) + '</CrimeCount></Crime>')
                    elif 'left:353.1pt' in line or 'left:346.8pt' in line or '350.0pt' in line:
                        output_file.write('<COUNT>' + re.sub(r'<.*?>', '', line.strip()) + '</COUNT>\n')

#create an html file extracted from the pdf
files = [f for f in os.listdir('pdfData') if os.path.isfile(os.path.join('pdfData', f)) and not f.startswith('.')]

for file in files:
    pdf_to_html('pdfData/'+file, 'parsing.html')
    html_to_text('parsing.html', 'parsing.txt')
    extract('parsing.txt', file.replace(".pdf", ".xml"))