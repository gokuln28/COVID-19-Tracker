import pandas as pd
import logging
import configparser


# Configuration file initialization
config = configparser.ConfigParser()
config.read('config.txt')

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
pd.set_option('display.width', 500)

# Logging configuration
logging.basicConfig(filename=config['datalog']['filename'], filemode=config['datalog']['filemode'],
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
streamhandler = logging.StreamHandler()
loggings = logging.getLogger()
formatter = logging.Formatter("%(levelname)s - %(message)s")
streamhandler.setFormatter(formatter)
loggings.addHandler(streamhandler)


coviddata = pd.read_csv("covidcases.csv")

# print(coviddata)

coviddata['Fatality Rate(%)'] = round(coviddata['Deaths'].astype(float) * 100 / coviddata['Confirmed cases'], 2)
coviddata['Survival Rate(%)'] = round(coviddata['Cured/Discharged'].astype(float) * 100 /
                                      coviddata['Confirmed cases'], 2)
totalconfirmedcases = coviddata['Confirmed cases'].sum()
totalcuredcases = coviddata['Cured/Discharged'].sum()
totaldeaths = coviddata['Deaths'].sum()
currentcases = totalconfirmedcases - totalcuredcases - totaldeaths
avgfatalityrate = round(coviddata['Fatality Rate(%)'].mean(), 3)
avgsurvivalrate = round(coviddata['Survival Rate(%)'].mean(), 3)
mostcasesstate = coviddata[coviddata['Confirmed cases'] == coviddata['Confirmed cases'].max()]
mostcasesstatename = mostcasesstate['Name of State / UT']

logging.info(f"Total Confirmed cases in India: {totalconfirmedcases}")
logging.info(f"Total Cured cases in India: {totalcuredcases}")
logging.info(f"No of current cases in India: {currentcases}")
logging.info(f"Total Deaths in India: {totaldeaths}")
logging.info(f"State with most cases in India: {mostcasesstatename}")
logging.info(f"Average fatality rate in India: {avgfatalityrate}")
logging.info(f"Average survival rate in India: {avgsurvivalrate}")
