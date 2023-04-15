#Agent Factory - Create Adjacency Matric
#Creates an adjacency matrix of agent to agent connections

#Author: Erik Connerty
#Date: 1/26/2023
#For the USC AI - Institute

import pandas as pd
import numpy as np
import constants
from tqdm.auto import tqdm

#Trust score scalar
scalar = 1.0/constants.NUM_OF_ATTRIBUTES

print('Starting...')

#Read the two necessary files into data frames
df1 = pd.read_csv(constants.AGENT_FILE_NAME,sep='~')
df2 = pd.read_excel(constants.INFO_SOURCE_FILE_NAME,skiprows=1,sheet_name=None)

ids_list = [] #maybe use sets here?
type_list = []
ids_to_type = dict()

#Get info sources to put in the matrix
for name, sheet in df2.items():
    sheet.rename(columns=str.lower, inplace=True) #Ensure the columns are lowercase
    ids_list.extend([s.strip() for s in sheet['source'].tolist()])
    type_list.extend([s.strip() for s in sheet['type'].tolist()])
    ids_to_type = dict(zip(ids_list, type_list))
 
ids_to_type = {k.lower(): v.lower() for k, v in ids_to_type.items()} #makes all lower case
ids_list = [*set(ids_list)] #Remove duplicate info sources from list
ids_list = [x.lower() for x in ids_list]  



#Extra step to write info sources to separate file
f1 = open(constants.INFO_DISS_FILE_NAME,'w')
f1.write('id~type~source\n')
for x in ids_to_type:
    f1.write(x +'~information-diss-agents~'+ids_to_type.get(x)+'\n')
f1.close()

# Create the list of agents for the matrix
matrix_list = [s.strip() for s in df1['id'].tolist()]
matrix_rows = matrix_list[:]  # The rows do not need to be extended with the ids_list, so we copy just the agents before extending it
matrix_list.extend(ids_list)

# Write the columns and rows(index)
matrix = np.zeros(shape=(len(matrix_list), len(matrix_rows)), dtype=float)
matrix[:] = 0.0
matrix_columns = matrix_rows
matrix_index = matrix_list

# Iterate the agents and populate the matrix with values
for index, row in df1.iterrows():
    idas = row['Information Dissemination Agents'].replace(', ', ',').strip('][').split(',')
    for source in idas:
        source = source.strip('\'').lower()
        if(source):
            if row['id'].__contains__('B-ID'):
                matrix[matrix_index.index(source), matrix_columns.index('B-ID-'+str(index+1))] = 1.00
            else:
                matrix[matrix_index.index(source), matrix_columns.index(row['id'])] = 1.00

#Numpy
# Create a dictionary that maps column names to their index in the NumPy array
col_indices = {col_name: i for i, col_name in enumerate(df1.columns)}

# Populate weights for agent to agent connections
# Convert df1 to a NumPy array
data = df1.to_numpy()

for i in tqdm(range(len(data)),desc='Creating Adjacency Matrix'):
    row = data[i]
    for j in range(i + 1, len(data)):
        row2 = data[j]
        trust_score = 0.0
        # Special case to check for municipality
        if row[col_indices['municipality']] == row2[col_indices['municipality']]:
            trust_score += scalar
        for k in range(constants.NUM_OF_SPECIAL_ATTRIBUTES, len(row)-1):  
            # Check if the attribute values are the same
            if row[k] == row2[k]:
                trust_score += scalar
        # Write the trust score value for that agent
        matrix[i, j] = trust_score
        matrix[j, i] = trust_score

print('Writing matrix to file...')
matrix = np.around(matrix, decimals=2)

# Create the data frame
matrix = pd.DataFrame(matrix, index=matrix_index, columns=matrix_columns)
        
#Write the adjacency matrix to a file
f = open(constants.ADJACENCY_MATRIX_FILE_NAME,'w',encoding="utf-8")
matrix.fillna('0.0', inplace=True)
f.write(matrix.to_csv(index=True,lineterminator='\n',sep='~'))
f.close()

print('Done!')
