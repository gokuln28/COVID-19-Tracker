from bs4 import BeautifulSoup
from urllib import request, error
import configparser
import csv
import logging
import sys

# Configuration file initialization
config = configparser.ConfigParser()
config.read('config.txt')

# Logging configuration
logging.basicConfig(filename=config['loggingconfig']['filename'], filemode=config['loggingconfig']['filemode'],
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
streamhandler = logging.StreamHandler()
loggings = logging.getLogger()
formatter = logging.Formatter("%(levelname)s - %(message)s")
streamhandler.setFormatter(formatter)
loggings.addHandler(streamhandler)

# Get the response from the "Ministry of Health and Family" website
URL = config['website']['url']
try:
    page = request.urlopen(URL)
except error.URLError:
    logging.error("Cannot get the response from the website.")
    sys.exit(1)
except Exception:
    logging.error("An unknown error has occured")
    sys.exit(1)
else:
    logging.info("Response received successfully")

soup = BeautifulSoup(page, 'html.parser')

# Parse the data from the "table" tag through "div" tag
parentDivTag = soup.find("div", {"class": config['htmltagclasses']['divclass']})
tableTag = parentDivTag.find('table', {"class": config['htmltagclasses']['tableclass']})
table_rows = tableTag.find_all('tr')

# Initializing list and row count to write to file
result = []
row_count = 0

# populating table data as list transform table data for CSV file
for tr in table_rows:
    td = tr.find_all('td')
    row = [individualrow.text.replace('\n', '').replace('#', '').
               replace('*States wise distribution is subject to further verification and reconciliation', '')
           for individualrow in td]
    # Append the individual lists to a single list
    if len(row) < 5:
        continue
    if len(row) == 5:
        row.insert(0, str(row_count + 1))
    result.append(row)
    row_count += 1
logging.info("Data parsed and appended to list")

# Initialize table headings and filename
headings = ["S.No", "State Id", "Name of State / UT", "Confirmed cases", "Cured/Discharged", "Deaths"]
filename = config['csv_file']['filename']

# Write to the file
try:
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headings)
        csvwriter.writerows(result)
except PermissionError:
    logging.error("CSV file is opened while writing. Try closing the file")
    sys.exit(1)

logging.info("Data written into csv file")
