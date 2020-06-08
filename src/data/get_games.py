import requests, bs4
import pandas as pd
import datetime

BASE_URL = 'https://howlongtobeat.com/'
game_name=""

headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*'
        }
payload = {
    'queryString': game_name,
    't': 'games',
    'sorthead': 'popular',
    'sortd': 'Normal Order',
    'plat': '',
    'length_type': 'main',
    'length_min': '',
    'length_max': '',
    'detail': '0'
}

min_page = 1
max_page = 2037
#2037
#manually searching https://howlongtobeat.com/#search2037 is ok but 2038 is not ok
#

page_range = range(min_page, max_page+1)

list_game_url=[]

print(datetime.datetime.now(),": Getting Id ...")
for page_id in page_range:
  print(page_id, "/", max_page)

  SEARCH_URL = BASE_URL + "search_results?page="+str(page_id)

  # Make the post request and return the result if is valid
  r = requests.post(SEARCH_URL, data=payload, headers=headers)
  game_path="https://howlongtobeat.com/"

  if r is not None and r.status_code == 200:
    soup=bs4.BeautifulSoup(r.text,'html.parser')
    games =soup.select('div.search_list_image > a')
    #print(page_id,games[0].get('aria-label'))

    for game in games:
      #print(game,'\n\n')
      game_id=game.get('href')
      game_link = game_path+game_id
      list_game_url.append(game_link)
      #print(game,"\n\n",game_id, ":", game.get('div'))

  else:
    print(r.status_code)

print(datetime.datetime.now(), ": Game URLs writing to list_game_url.csv ...")

game_url_df = pd.DataFrame(list_game_url)
game_url_df.to_csv('list_game_url.csv', sep=',', header=None, index=None)


all_game_df=pd.DataFrame()

count=0
dim = len(list_game_url)

print(datetime.datetime.now(), ": Starting to loop through games ... There are ", dim, " number of games ...")

for game_link in list_game_url:
    print(count, " out of ",dim)
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

    if len(game_get_times)<=0:
        break
    else:

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
    """ publisher et al info 

    		# Profile (game information).
		profile = {
			'Type': '',
			'Developers': '', # includes both 'Developer' and 'Developers'
			'Publishers': '', # includes both 'Publisher' and 'Publishers'
			'Playable On': '',
			'Genres': '', # includes both 'Genre' and 'Genres'
			'NA': '',
			'EU': '',
			'JP': ''
		}

    """

    all_game_df = pd.concat([all_game_df, game_df],
                            sort=False, ignore_index=True)

all_game_df.sort_values('Title', inplace=True)
all_game_df.reset_index(inplace=True)


print(all_game_df)

all_game_df.to_csv('all-games.csv', index=None)
print(datetime.datetime.now(), ": DONE !")
