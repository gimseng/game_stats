# Get Data

This documentation provides details of the Python codes needed to generate the data in [data/raw](https://github.com/gimseng/game_stats/blob/master/data/raw).

There are three steps to the process:
1. [get_game_list.py](https://github.com/gimseng/game_stats/blob/master/src/data/get_game_list.py): 
The website contains a search function whereby if no search text is enetered, it will generate all the game with their summary info. This code makes use of this to allow us to obtain their game ID and store them (or rather the link to each of the game's page) in a list (which is in the [list_game_url.csv](https://github.com/gimseng/game_stats/blob/master/data/interim/list_game_url.csv) file). Eventually, the code sets up all the game links we will have to scrap in the next stage. The most challenging part for me was to figure out how to deal with AJAX. Eventually, after understanding it, it seems rather straighforward to pass headers and payload data to request the dynamically generated pages.

2. [get_game_info.py](https://github.com/gimseng/game_stats/blob/master/src/data/get_game_info.py): 
For each game link generated in the first step, we then scrap the webpage. This is a rather time-consuming task, since it has to scrap through order of thousands of webpages. It took about 3 hours when I ran it. The scraping is rather straighforward but sometimes the data are not always consistent. For e.g. time played might be entere '13h' vs '13 hours' and sometimes for never-ending games, it has entries like '200-400 hours'. At this point, there is some minimal data cleaning which have been done, but I will leave the majority of data cleaning to the later stage of the project. A majority of the work involves figuring out where the texts of relevance are stored in the html hierarchy. A bit of patient and a lot of browser developer's inspect were needed to construct the codes. The output of the code is a list of games with their information, stored in [all_game.csv](https://github.com/gimseng/game_stats/blob/master/data/raw/all_game.csv)


3.
