import requests
import bs4
import pandas as pd
import numpy as np

import datetime
import random

#pd.set_option('display.max_columns', 100)
#pd.set_option('display.width', 100)

SAVE_FILE_PATH = '/Users/gng/Google Drive/my own projects/gaming/game_stats/data/raw/'

all_game_df = pd.DataFrame()
count = 1

start_time = datetime.datetime.now()


list_game_df = pd.read_pickle(SAVE_FILE_PATH+"list_game_url.pkl")
list_game_url = list_game_df.values.tolist()

dim = len(list_game_url)
print("Starting time at : {}. Starting to loop through games ... There are {} number of games.".format(
    start_time.strftime("%Y-%m-%d, %H:%M"), dim))


for game_link_pre in list_game_url:

    game_link = game_link_pre[0]

    if count % 400 == 0:
        timesince = datetime.datetime.now() - start_time
        minutessince = int(float(timesince.total_seconds() / 60))
        print_str = "Total time so far: {} mins. Progress: {} % ({} / {})".format(str(
            minutessince), str(int(100*(count+1)/len(list_game_url))), str(count), str(len(list_game_url)))
        print("\r {}".format(print_str), end="")
    count += 1

    game_df = pd.DataFrame()
    game_id = game_link.split('=')[1]

    res = requests.get(game_link)
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    game_get_title = noStarchSoup.select('div.profile_header')
    game_get_times = noStarchSoup.select('div.game_times')

    game_title = game_get_title[0].getText()

    game_df['Id'] = [game_id]
    game_df['Title'] = [game_title[1:]]

    if len(game_get_times) > 0:

        game_time_list = game_get_times[0].select('li')

        for game_time in game_time_list:
            game_time_type = game_time.select('h5')[0].getText().strip()
            game_time_value = game_time.select('div')[0].getText().strip()

            # Strip all spaces, replace '--' with 'NA', replace '1/2' with '.5'.
            game_time_value = game_time_value.replace(
                '--', '').replace('½', '.5')

            # There are two time formats: 'Mins' and 'Hours'.
            # If 'Mins', strip and convert into a fraction of hours, but convert back to string for consistency.
            # If 'Hours', just strip.

            if len(game_time_value.split()) > 0:
                if len(game_time_value.split()) == 2:
                    game_time_value_type = game_time_value.split()[-1]
                elif len(game_time_value.split()) == 1:
                    if game_time_value.split()[0][-1] == 'h':
                        game_time_value_type = 'Hours'
                else:
                    game_time_value_type = 'Unknown'

                if len(game_time_value.split()) == 2:
                    game_time_actual_value = game_time_value.split()[0]
                elif len(game_time_value.split()) == 1:
                    game_time_actual_value = game_time_value.split()[0][:-1]

                if game_time_value_type == "Hours" or game_time_value_type == 'h':
                    new_game_time_value = game_time_actual_value.replace(
                        game_time_value_type, '')

                elif game_time_value_type == "Mins":
                    new_game_time_value = float(game_time_actual_value)/60.0
                else:
                    game_time_value_type = "Unknown"
                    new_game_time_value = game_time_value
            else:
                game_time_value_type = "Unknown"
                new_game_time_value = game_time_value

            try:
                if not(str(new_game_time_value).isspace()):
                  new_game_time_value = round(float(new_game_time_value), 2)
                else:
                  new_game_time_value = np.nan
            except:
                pass

            game_df[game_time_type] = [new_game_time_value]

        if len(noStarchSoup.select('div.game_chart > h5')) > 0:
            game_rating = noStarchSoup.select('div.game_chart > h5')[
                0].getText()[:-8]
            game_retired = noStarchSoup.select('div.game_chart > h5')[1]

            # some bad '\br' things going on, so replace and then strip.

            for br in game_retired.select('br'):
                br.replace_with(', ')
            game_retired = game_retired.getText().split(',')[1][:-1]
        else:
            game_rating = ''
            game_retired = ''
        game_df['Rating'] = game_rating
        game_df['Retired'] = game_retired

    profile_info = noStarchSoup.select('div.profile_info')

    for info in profile_info:

        info_type = info.select('strong')[0].getText().split('\n')
        info_type = list(filter(None, info_type))[0]

        info_value = info.getText().split('\n')
        info_value = list(filter(None, info_value))

        if len(info_value) > 1:
            info_value = info_value[-1]
        else:
            info_value = info_value[0]
        info_type = info_type.replace(':', '')
        info_value = info_value.replace(':', '')

        info_value = info_value.replace(info_type, '')
        if info_type[-1] == 's':
            info_type = info_type[:-1]
        info_type = info_type.strip()

        game_df[info_type] = info_value

    all_game_df = pd.concat([all_game_df, game_df],
                            sort=False, ignore_index=True)

all_game_df.sort_values('Title', inplace=True)
all_game_df.reset_index(inplace=True, drop=True)

print(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"), ": DONE !")


all_game_df.to_csv(SAVE_FILE_PATH+'all_game_df.csv', sep=',')
all_game_df.to_pickle(SAVE_FILE_PATH+'all_game_df.pkl')

# some games are not "beatable". Note: this game has been flagged as sports/unbeatable. Some statistics will be combined.
