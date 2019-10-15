import pandas as pd
import numpy as np
''' Dataset downloaded from kaggle and code
    was pulled off of Kaggle courtesy of Pietro Pozzati
    Edited further for analysis by Jonathan Hercules
'''

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
x = [value[value != None]  for value in results.values]
match['result']= x
match['result']=np.squeeze(match.result.tolist())

#home
home_teams=match.groupby(['home_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})

home_matches=[]
for team in home_teams.home_team:
    tot_matches= home_teams[home_teams.home_team== team]['count'].sum()
    home_matches.append(tot_matches)


home_teams['home_matches'] = home_matches
home_teams['home_pct_win'] = np.around(home_teams['count']/ home_teams['home_matches'] * 100,decimals=2)

away_teams=match.groupby(['away_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})
away_teams.replace({'loss':'win', 'win':'loss'})

away_tot_matches=[]
for team in away_teams.away_team:
    tot_matches= away_teams[away_teams.away_team == team]['count'].sum()
    away_tot_matches.append(tot_matches)

away_teams['away_matches']= away_tot_matches
away_teams['away_pct_win'] = np.around(away_teams['count']/away_teams['away_matches'] * 100, decimals=2)

home_teams.rename(columns={'result': 'results', 'count': 'home_count'}, inplace=True)
home_teams.set_index('home_team', inplace=True)
away_teams.rename(columns={'result': 'results', 'count': 'away_count'}, inplace=True)
away_teams.set_index('away_team', inplace=True)

#defining winners and loosers
home_winners= home_teams[home_teams.results=='win']
away_winners= away_teams[away_teams.results=='win']

home_losers= home_teams[home_teams.results=='loss']
away_losers= away_teams[away_teams.results=='loss']

#merging datasets
columns_ = ['home_count','away_count', 'home_matches', "away_matches",'results_x','results_y']
winners=pd.merge(home_winners, away_winners, left_index=True, right_index=True,how='inner')
winners['total_amount_won'] = winners['home_count'] + winners['away_count']
winners['total_matches'] = winners['home_matches'] + winners['away_matches']

losers = pd.merge(home_losers,away_losers,left_index=True,right_index=True,how='inner')
losers['total_amount_lost'] = losers['home_count'] + losers['away_count']
losers['total_matches'] = losers['home_matches'] + losers['away_matches']
losers.rename(columns = {'home_pct_win':'home_pct_lost', 'away_pct_win':'away_pct_lost'},inplace=True)


winners = winners.drop(columns_, axis =1 )
losers = losers.drop(columns_,axis = 1)


print(winners)



