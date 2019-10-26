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


#home
home_teams=match.groupby(['home_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})

home_matches=[]
for team in home_teams.home_team:
    tot_matches= home_teams[home_teams.home_team== team]['count'].sum()
    home_matches.append(tot_matches)
    
 
   
home_teams['home_matches']=home_matches
home_teams['pct_home_victory']= np.round(home_teams['count']/ home_teams['home_matches'] * 100,2)


#away
away_teams=match.groupby(['away_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})
away_teams.replace({'loss': 'win', 'win':'loss'}, inplace=True) #loss means victory for the away team

away_tot_matches=[]
for team in away_teams.away_team:
    tot_matches= away_teams[away_teams.away_team == team]['count'].sum()
    away_tot_matches.append(tot_matches)

away_teams['away_matches']= away_tot_matches
away_teams['pct_victory_away'] = away_teams['count']/away_teams['away_matches']


#adjusting terminology and index
home_teams.rename(columns={'result': 'home_results', 'count': 'home_count'}, inplace=True)
home_teams.set_index('home_team','Team', inplace=True)
away_teams.rename(columns={'result': 'away_results', 'count': 'away_count'}, inplace=True)
away_teams.set_index('away_team','Team', inplace=True)

#defining winners and losers
home_winners= home_teams[home_teams.home_results=='win']
away_winners= away_teams[away_teams.away_results=='win']
home_losers= home_teams[home_teams.home_results=='loss']
away_losers= away_teams[away_teams.away_results=='loss']


#merging datasets
winners=pd.merge(home_winners, away_winners, left_index=True, right_index=True, how='inner')
#losers=pd.merge(home_losers, away_losers, left_index=True, right_index=True, how='inner')
#losers.rename(columns={'pct_home_victory': 'pct_home_defeats', 'pct_victory_away': 'pct_away_defeats'}, inplace=True)

columns_ = ['home_count','away_count', 'home_matches', "away_matches"]
winners['tot_count']= winners.home_count + winners.away_count
winners['tot_matches']= winners.home_matches + winners.away_matches
winners['tot_pct_victory']= np.round(winners.tot_count/winners.tot_matches*100,2)


winners = winners[['tot_count','tot_pct_victory']]
winners = winners.sort_values(by='tot_pct_victory',ascending=False)

teams = winners_.index.to_numpy()
values = list(winners_["tot_pct_victory"])
fig, axs = plt.subplots(figsize=(20, 10), sharey=True)
plt.bar(teams[:100],values[:100])
