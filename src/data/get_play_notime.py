import requests
import bs4
import pandas as pd
import numpy as np

import datetime
import time
import random

#pd.set_option('display.max_columns', 100)
#pd.set_option('display.width', 100)

SAVE_FILE_PATH = '/content/drive/My Drive/personal projects/gaming/game_stats/data/interim/notime/'

#all_game_df = pd.DataFrame()
count = 1

start_time = datetime.datetime.now()

list_game_source = "https://raw.githubusercontent.com/gimseng/game_stats/master/data/interim/list_game_url.pkl"
list_game_df = pd.read_pickle(list_game_source)
list_game_url = list_game_df.values.tolist()

dim = len(list_game_url)
print("Starting time at : {}. Starting to loop through games ... There are {} number of games.".format(
    start_time.strftime("%Y-%m-%d, %H:%M"), dim))


BASE_URL = 'https://howlongtobeat.com/'

for game_link_pre in list_game_url:

  all_play_df = pd.DataFrame()

  game_link = game_link_pre[0]

  if count % 40 == 0:
      timesince = datetime.datetime.now() - start_time
      minutessince = int(float(timesince.total_seconds() / 60))
      print_str = "Total time so far: {} mins. Progress: {} % ({} / {})".format(str(
          minutessince), str(int(100*(count+1)/len(list_game_url))), str(count), str(len(list_game_url)))
      print("\r {}".format(print_str), end="")
      time.sleep(2.5)

  count += 1

  game_id = game_link.split('=')[1]

  completion_game_link = 'https://howlongtobeat.com/game.php?id=%s&s=completions' % game_id

  res = requests.get(completion_game_link)
  noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')

  try:
    find_div = noStarchSoup.select("div[id=\"completion_times_4\"]")[0]
    num_play_private = len(find_div.select("span"))
    no_time_user = find_div.select("a")
    no_time_user_list = [item.getText() for item in no_time_user]

    SAVE_FILE_NAME = SAVE_FILE_PATH+'all_play_no_time_'+str(game_id)+'.txt'
    with open(SAVE_FILE_NAME, 'w') as f:
      f.write("%s\n" % num_play_private)
      f.write("%s\n\n" % len(no_time_user_list))

      for item in no_time_user_list:
        f.write("%s\n" % item)
  except:
    pass
  #print(datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"),": saving file ",SAVE_FILE_NAME,"...")
