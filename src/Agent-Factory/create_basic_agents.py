#Agent Factory - Basic Agents
#This program will read in an input file and generate basic agents using python's built in random probability functions.

#Author: Erik Connerty
#Date: 1/1/2023
#For the USC AI - Institute

#Imported Libraries
import pandas as pd
from decimal import *
import random
import constants
from tqdm import tqdm

print('Starting...')

#Read in the files to be processed
sheets = pd.read_excel(constants.ATTRIBUTE_FILE_NAME,sheet_name=None)
attributes = sheets.pop('Attributes')
attributes.rename(columns=str.lower, inplace=True) #Ensure the columns are lowercase

#Open the output file to be written to
f = open(constants.AGENT_FILE_NAME,'w')
f2 = open(constants.SPOKESPERSON_LIST_OUTPUT,'w')

#Write the header/topline for the agent attributes
#Write sheet name columnn for later
out = 'sheet~'
out += 'id~'+'type~'
for i in range (0,len(attributes.index)):
    out +=attributes.get('attribute')[i] + '~'
out = out.rstrip(out[-1])
out = out.replace('population_share~','')
#out = out.replace('Coordinates,','Latitude,Longitude,') #Implement requested changes for Mike
#out2 = out + ',triad_stack_id,simulation_id\n' #Some fudgery to get the header right on spokesperson out
out += '\n'
out2 = out.replace('sheet~','')
f.write(out)
f2.write(out2)
out = ''


#Extra step to write spokesperson output file
spokesperson_list = pd.read_csv(constants.SPOKESPERSON_LIST_FILE_NAME,sep='~')
spokesperson_list.drop(columns=[spokesperson_list.columns[-1]],inplace=True)
f2.write(spokesperson_list.to_csv(index=False,lineterminator='\n',sep='~'))
f2.close()



#Create the agents using a loop
attributes_list = []
agent_id = 1
for name in tqdm(sheets,desc='Creating Agents'):
    municipality = sheets[name]
    municipality.rename(columns=str.lower, inplace=True) #Ensure the columns are lowercase
    num_of_agents = int(round((Decimal(municipality.get('value01')[5]) / Decimal(100)) * Decimal(constants.TOTAL_NUM_OF_AGENTS), 0)) #TODO: Stop using magic numbers. 5 is population_share

    for i in range(num_of_agents):
        # Write the name of the sheet so that I can get it back later
        out = name + '~'

        # Write the agents identifier information
        isDonovian = str(municipality.get('value01')[2])[0].isdigit() #Distinguishes donovian agents from basic agents using municipality name as a marker
        out += f"B-ID-{agent_id}~{'donovian' if isDonovian else 'basic'}~"

        # Writes out the country, county, municipality, and coordinates
        out += f"{municipality.get('value01')[0]}~{municipality.get('value01')[1]}~{municipality.get('value01')[2]}~{municipality.get('value01')[3]}~{municipality.get('value01')[4]}~"

        # Calculate the attributes
        attributes_list = [attributes[str(random.choices(list(row.iloc[1:].dropna().index), weights=row.iloc[1:].dropna().values)[0])].get(index) for index, row in municipality.iloc[constants.ATTRIBUTE_TEMPLATE_OFFSET:].iterrows()]
        out += '~'.join(attributes_list) + '~'

        out = out.rstrip('~') + '\n'
        with open(constants.AGENT_FILE_NAME, 'a') as f:
            f.write(out)
        
        agent_id += 1

f.close()

#Extra step to write the preliminary basic agent input
agents = pd.read_csv(constants.AGENT_FILE_NAME,sep='~')
agents.drop(columns=['sheet'],inplace=True)
agents['triad_stack_id'] = ''
agents['simulation_id']  = ''
f = open(constants.BASIC_AGENT_FILE_NAME,'w')
f.write(agents.to_csv(index=False,lineterminator='\n'))

print("Done!")