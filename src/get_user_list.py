import requests
import bs4
import pandas as pd
import datetime



BASE_URL = 'https://howlongtobeat.com/'
SAVE_FILE_PATH = '/Users/gng/Google Drive/my own projects/gaming/game_stats/data/interim/user/'
game_name = ""

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*'
}
payload = {
    'queryString': game_name,
    't': 'users',
    'sorthead': 'postcount',
    'sortd': 'Normal Order',
    'plat': '',
    'length_type': 'main',
    'length_min': '',
    'length_max': '',
    'detail': ''
}

min_page = 1
#max_page=2
max_page = 11754

# manually searching https://howlongtobeat.com/#search11754 is ok but 11755 is not ok. As of Jun 22, 2020.
# maybe write another code to find this value later on

page_range = range(min_page, max_page+1)

list_user_url = []

start_time = datetime.datetime.now()
print("Starting time at : {}. Getting user id and links ...".format(
    start_time.strftime("%Y-%m-%d, %H:%M")))

for page_id in page_range:
    if page_id % 100 == 0:
        timesince = datetime.datetime.now() - start_time
        minutessince = int(float(timesince.total_seconds() / 60))
        print_str = "Total time so far: {} mins. Progress: {} % ({} / {})".format(str(
            minutessince), str(int(100*int(page_id)/len(page_range))), str(page_id), str(len(page_range)))

        print("\r {}".format(print_str), end="")

    SEARCH_URL = BASE_URL + "search_results?page="+str(page_id)

    # Make the post request and return the result if is valid
    r = requests.post(SEARCH_URL, data=payload, headers=headers)

    if r is not None and r.status_code == 200:
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        user_item_list = soup.select('div.search_list_image>a')
        
        for user_item in user_item_list:
            user_name = user_item.get('title')
            user_link = BASE_URL+user_item.get('href')
            list_user_url.append(user_link)

print(datetime.datetime.now(), ": Game URLs writing to list_user_url.csv ...")

game_url_df = pd.DataFrame(list_user_url)
game_url_df.to_csv(SAVE_FILE_PATH+'list_user_url.cs',
                   sep=',', header=None, index=None)
game_url_df.to_pickle(SAVE_FILE_PATH+'list_user_url.pkl')
