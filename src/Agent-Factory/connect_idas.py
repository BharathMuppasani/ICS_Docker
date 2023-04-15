#Agent Factory - Connect Information Dissemination Agents
#Connects basic agents to information sources using the given input files.

#Author: Erik Connerty
#Date: 1/1/2023
#For the USC AI - Institute

import pandas as pd
from pandas import DataFrame
from decimal import Decimal
import random
import constants
from tqdm.auto import tqdm

# Enable progress_apply for pandas DataFrames
tqdm.pandas(desc='Connecting info sources')

print('Starting...')

# Preprocess the sheets
sheets = pd.read_excel(constants.ATTRIBUTE_FILE_NAME, sheet_name=None, index_col=0)
headerSheet = sheets.pop('Attributes').rename(columns=str.lower)

# Preprocess the municipality sheets
municipality_sheets = {k: v.rename(columns=str.lower) for k, v in sheets.items()}

# Calculate the total population share for each country
pop_share = {country: sum(sheet.at['population_share', 'value01'] for sheet in municipality_sheets.values() if sheet.at['country', 'value01'].lower() == country) for country in ['lithuania', 'estonia', 'latvia', 'poland', 'belarus']}

# Read the agent file
df = pd.read_csv(constants.AGENT_FILE_NAME, sep='~')

# Preprocess the info source sheets
info_source_sheets = {}
for country in ['lithuania', 'estonia', 'latvia', 'poland', 'belarus']:
    try:
        sheet_data = pd.read_excel(constants.INFO_SOURCE_FILE_NAME, sheet_name=country.strip(), header=[0,1], skiprows=0)
        info_source_sheets[country] = sheet_data
    except:
        info_source_sheets[country] = None

# Define the function to process each row in the DataFrame
def process_agent_row(row: pd.Series):
    municipalitySheet = municipality_sheets[row['sheet']]
    agent_values= []
    agent_percentage = 1.0

    for i in range(constants.NUM_OF_SPECIAL_ATTRIBUTES, len(row)): # -1 to exclude the last column which is the info sources
        rowName = row.index[i]
        rowValue = row[i]
        rowValues = municipalitySheet.loc[rowName]
        columnIndex = headerSheet.columns[(headerSheet.loc[rowName] == rowValue).values]
        value = municipalitySheet.loc[rowName, columnIndex].iloc[0]
        agent_percentage *= float(value)/100.0

    country = municipalitySheet.at['country', 'value01'].lower()
    agent_percentage *= (float(pop_share[country]) / 100) * len(df)

    # Compute information source percentage
    df2: DataFrame = info_source_sheets[country]
    spokepersons_list = []

    for index, info_source in df2.iterrows():
        countryPercentage = info_source.iloc[3]
        source_percentage = 1.0

        # Probability weight for each attribute from information source
        for i in range(constants.NUM_OF_SPECIAL_ATTRIBUTES, len(row)):
            rowName = row.index[i]
            rowValue = row[i]
            if rowValue != '[]':
                source_value = info_source[rowName, rowValue]
                source_percentage *= float(source_value)
        # Get the total number of the population for that news source
        source_percentage *= ((float(pop_share[country]) / 100) * len(df)) * float(countryPercentage)

        if random.random() < source_percentage / agent_percentage:
            spokepersons_list.append(str(info_source[0]).strip())

    return str(spokepersons_list)

# Apply the function to each row in the DataFrame
df['Information Dissemination Agents'] = df.progress_apply(process_agent_row, axis=1)


#Write the tmp file
f = open(constants.AGENT_FILE_NAME,'w')
df.drop(columns=['sheet'],inplace=True)
f.write(df.to_csv(index=False,lineterminator='\n',sep='~'))
f.close()

#Write the basic agent output
df.drop(columns=['Information Dissemination Agents'],inplace=True)
df['triad_stack_id'] = ''
df['simulation_id']  = ''
f = open(constants.BASIC_AGENT_FILE_NAME,'w')
f.write(df.to_csv(index=False,lineterminator='\n',sep='~'))
f.close()

#Print
print('Done!')


#Append the spokespersons to the csv
f1 = open(constants.AGENT_FILE_NAME,'a+')
f2 = open(constants.SPOKESPERSON_LIST_FILE_NAME,'r')
f1.write(f2.read())
f1.close()
f2.close()
    
