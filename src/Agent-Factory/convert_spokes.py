import pandas as pd
from decimal import *
import random
import constants

spokes = pd.read_csv(constants.SPOKESPERSON_LIST_FILE_NAME)

f =open(constants.SPOKESPERSON_LIST_FILE_NAME,'w')

f.write(spokes.to_csv(index=False,lineterminator='\n',sep='~'))