############## Inputs ########################
#Inputs from the identity team
ATTRIBUTE_FILE_NAME = './Data/V4.0 Redzone Attribute Template + Demographic Tables (Database Compatible).xlsx'
#ATTRIBUTE_FILE_NAME = './Data/Donovian Soldier Data V3.0 (3.20.23).xlsx'
INFO_SOURCE_FILE_NAME = './Data/Group+InfoSource V4.0 (5% min)(working).xlsx'

#An input created by me that may or may not come from the identity team in the correct format
SPOKESPERSON_LIST_FILE_NAME = './Data/spokesperson_v2.0.csv'
############## Inputs #########################

####################### Temp Files ############################
#Temp File
AGENT_FILE_NAME = './Data/agents.csv' #This is just a temp file used by the program, not an actual output.
####################### Temp Files ############################

##################### Outputs ############################
#Outputs
ADJACENCY_MATRIX_FILE_NAME =  '/home/data/input/adjacency_matrix.csv'
INFO_DISS_FILE_NAME = '/home/data/input/InfoDissAgents.csv'
SPOKESPERSON_LIST_OUTPUT = '/home/data/input/spokespersonAgentsInput.csv'
BASIC_AGENT_FILE_NAME = '/home/data/input/basicAgentsInput.csv'
##################### Outputs ############################

######################## Agents to be created ############################
#Agent total
#Depending on what is provided as input, this number may not be perfectly adhered to, and a few more or a few less agents may be created.

TOTAL_NUM_OF_AGENTS = 200
######################## Agents to be created ############################

######################## Configurations ############################
#Number of attributes

#This is for the adjacency matrix exclusively, and helps to calculate trust scores
#Will need to be changed if additional attributes are added to the end of the redzone attribute template
NUM_OF_ATTRIBUTES = 11 #This is how many attributes there are that have probabilities attached to them + 1 for Municipality. I.E All the attributes after lat long + 1
#For our current setup, this number should be 9 for basic agents, and 10 for donovian agents

#This is for calculating the offset for where the probabilistic attributes start
#So as of now, there are 8 attributes before Gender in the agent output file
#Likely will never need to be changed
NUM_OF_SPECIAL_ATTRIBUTES = 8 #sheet id type country county municipality lat long from the agent output = 8
#The sheet attribute is one created by the program, the rest are agent attributes

#This is set from the redzone attribute template, and has a different number because there is no id or type
#So if the template sheet is different, this could also be different, but likely will never need to be changed
#Also likely to never need to be changed.
ATTRIBUTE_TEMPLATE_OFFSET = 6 #country county municipality lat long population_share from the Attribute Template = 6
######################## Configurations ############################
