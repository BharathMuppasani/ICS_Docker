# ICS (Agent Factory)
This will create basic agents, connect them to Information Dissemination Agents, and then create an adjacency matrix of weighted values for each agent's connections.

# Requirements
* Requires Python version 3.10

# Inputs
The inputs required are the RedZone Attribute Excel SpreadSheet, the spokesperson's csv, and the Information Sources Excel SpreadSheet

# Instructions
1. Install the dependencies pandas numpy, and openpyxl for python with ```pip install pandas tqdm openpyxl```
2. Run ```python create_basic_agents.py```
3. Run ```python connect_idas.py```
4. Run ```python create_adjacency_matrix.py```

The output files are ```spokespersonAgentsInput.csv```, ```InfoDissAgents.csv```, ```basicAgentsInput.csv``` and ```adjacency_matrix.csv```.

Spokesperson agents must be predefined and in the format specified in the ```./Data/spokesperson.csv``` file.

All filenames and parameters are defined in the ```constants.py``` file.
