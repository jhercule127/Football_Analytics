import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
match= pd.read_csv('C:/Users/alcir/OneDrive/Documents/Football Analytics/results.csv')

#put date in correct format and set it as the index
date= pd.to_datetime(match.date.values)
match['date']=date
match.set_index('date', inplace=True)


#get the coloumn of results (wins, ties and losses)
win= np.where(match.home_score > match.away_score, 'win', None)
tie=np.where(match.home_score == match.away_score, 'tie', None)
loss= np.where(match.home_score < match.away_score, 'loss', None)

results=pd.DataFrame([win, tie, loss]).T
x=[value[value != None]  for value in results.values]

match['result']= x
match['result']=np.squeeze(match.result.tolist())

# Year 1 is the first year example 2000
# Year 2 is the second year example 2010
def getdecade_info(year_1,year_2):
    return match.loc['{}-1-1'.format(year_1):'{}-12-31'.format(year_2)]

decade = getdecade_info(2000,2010)
print(decade)
