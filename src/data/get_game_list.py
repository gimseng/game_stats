import requests, bs4
import pandas as pd
import datetime


def get_game_list():
        
    BASE_URL = 'https://howlongtobeat.com/'
    SAVE_FILE_PATH = '/Users/gng/Google Drive/my own projects/gaming/game_stats/data/interim/'
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
    max_page = 2042

    # manually searching https://howlongtobeat.com/#search2042 is ok but 2043 is not ok. As of Jun 9, 2020.
    # maybe write another code to find this value later on

    page_range = range(min_page, max_page+1)

    list_game_url=[]

    start_time=datetime.datetime.now()
    print("Starting time at : {}. Getting game id and links ...".format(start_time.strftime("%Y-%m-%d, %H:%M")))


    for page_id in page_range:
    if page_id%100==0:
        timesince = datetime.datetime.now() - start_time
        minutessince = int(float(timesince.total_seconds() / 60))
        print_str = "Total time so far: {} mins. Progress: {} % ({} / {})".format(str(
            minutessince), str(int(100*int(page_id)/len(page_range))), str(page_id), str(len(page_range)))

        print("\r {}".format(print_str), end="")


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
    game_url_df.to_csv(SAVE_FILE_PATH+'list_game_url.csv', sep=',', header=None, index=None)
    game_url_df.to_pickle(SAVE_FILE_PATH+'list_game_url.pkl')      
    
    return game_url_df

