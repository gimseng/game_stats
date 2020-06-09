import requests, bs4
import pandas as pd
import datetime

SAVE_FILE_PATH = '/Users/gng/Google Drive/my own projects/gaming/game_stats/data/raw/'

all_game_df=pd.DataFrame()
count = 1

start_time = datetime.datetime.now()


list_game_df = pd.read_pickle(SAVE_FILE_PATH+"list_game_url.pkl")
list_game_url = list_game_df.values.tolist()

dim = len(list_game_url)
print("Starting time at : {}. Starting to loop through games ... There are {} number of games.".format(
    start_time.strftime("%Y-%m-%d, %H:%M"), dim))

for game_link_pre in list_game_url:
    game_link=game_link_pre[0]
    if count % 100 == 0:
        timesince = datetime.datetime.now() - start_time
        minutessince = int(float(timesince.total_seconds() / 60))
        print_str = "Total time so far: {} mins. Progress: {} % ({} / {})".format(str(minutessince), str(int(100*(count+1)/len(list_game_url))), str(count), str(len(list_game_url)))
        print("\r {}".format(print_str), end="")
    count+=1

    game_df = pd.DataFrame()
    game_id=game_link.split('=')[1]

    res=requests.get(game_link)
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    game_get_title = noStarchSoup.select('div.profile_header')
    game_get_times = noStarchSoup.select('div.game_times')

    game_title = game_get_title[0].getText()

    game_df['Id'] = [game_id]
    game_df['Title'] = [game_title[1:]]

    if len(game_get_times)>0:

        game_time_list = game_get_times[0].select('li')

        for game_time in game_time_list:
            #print(game_title,game_time)
            game_time_type = game_time.select('h5')[0].getText()#+" (Hours)"
            game_time_value = game_time.select('div')[0].getText()

            # Strip all spaces, replace '--' with 'NA', replace '1/2' with '.5'.
            game_time_value = game_time_value.replace('--', '').replace('½', '.5')

            # There are two time formats: 'Mins' and 'Hours'.
            # If 'Mins', strip and convert into a fraction of hours, but convert back to string for consistency.
            # If 'Hours', just strip.
            
            if len(game_time_value.split())>0:
                game_time_value_type=game_time_value.split()[-1]
                game_time_actual_value = game_time_value.split()[0]

                if game_time_value_type == "Hours" or game_time_value_type=='h':
                    new_game_time_value = game_time_actual_value
                elif game_time_value_type=="Mins":
                    new_game_time_value = float(game_time_actual_value)/60.0
                else:
                    game_time_value_type="Unknown"
                    new_game_time_value = game_time_value
            else:
                new_game_time_value = game_time_value

            game_df[game_time_type] = [new_game_time_value]
        
        if len(noStarchSoup.select('div.game_chart > h5')) > 0:
            game_rating = noStarchSoup.select('div.game_chart > h5')[0].getText()[:-8]
            game_retired = noStarchSoup.select('div.game_chart > h5')[1]
            for br in game_retired.select('br'):
                br.replace_with(', ')
            game_retired=game_retired.getText().split(',')[1][:-1]
        else:
            game_rating=''
            game_retired=''

            # some bad '\br' things going on, so replace and then strip.


        game_df['Rating']=game_rating
        game_df['Retired'] = game_retired

    # to be done
    
    

    all_game_df = pd.concat([all_game_df, game_df],
                            sort=False, ignore_index=True)

all_game_df.sort_values('Title', inplace=True)
all_game_df.reset_index(inplace=True)


print(datetime.datetime.now(), ": DONE !")

all_game_df.to_csv(SAVE_FILE_PATH+'all_game_df.csv', sep=',', header=None, index=None)
all_game_df.to_pickle(SAVE_FILE_PATH+'all_game_df.pkl')

