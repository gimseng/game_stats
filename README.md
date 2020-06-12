# game_stats

Welcome to my gameplay data analysis project (which I call game_stats). In this project, I will be doing an end-to-end data science project, involving perhaps a few data engineering/machine learning modeling task. I am structuring the project in the following ways. I provide a quick summary for some parts, with further documentations (linked when needed) in the docs folder for further technical details.

## Motivations and Goals
<!--, Big Picture/Project Motivation, Problem Statement and Project Goals-->
The video game industry generates sales of > US$100 billion annually. It is perhaps one of the most important player in the entertainment sector. Therefore, leveraging data analytics to understand gamer behavior and spending trends is an important strategy to pursue. In this project, I will like to obtain, explore and build predictive models based on gamer playtime and rating. I will focus on consoles and PC gamers which traditional make up most of the gamers, though mobile gamers are definitely important for the future of gaming. The goals will be to provide clean data that are relevant for the following  big questions:

1. Do longer time provide more fun experience? Is this dependent on gender? My initial idea is for some games (like action adventure), as long as the quality (for e.g. a good story) is high, a shorter gameplay might be sufficient as long as it is an overall quality experience. For genres which focus on good gameplay mechanics, perhaps a longer playtime will be fun too. Games like Rocketleague, Minecraft or FIFA are simply more fun the more you play ! Uncovering this type of intuitions in the data through rigorous quantitative analysis will be enlightening as well as providing actionable questions into some aspects of game design.

2. We sometimes see developer ‘pad’ gameplay with somewhat unimpressive contents to artificially prolong gameplay time. Is this something that we can make quantitative in our data? What develovoper studios do this a lot? Can we cluster such games or developers? The impact will then inform developers to avoid such pitfalls, since it might also affect future sales (which is another question we might explore in our project).

3. How about gameplay fatigue? For each genre of video game, how long do people typically play before they quit or dislike the games? How to propose a quantitative measure and quantitatively answer this question is something which will be useful for game design as well. In particular, given the prominent of DLCs and episodic release of game chunks in AAA games, this will be a study to explore the benefits of splitting games into smaller releases.

4. Lastly, is there a meaningful way to cluster players based on playtime and perhaps rating? Could this provide a predictive machine learning model? Such a model could then be used for developers when they want to compare a certain playtime profile with another to decide how to proceed with their game development. If we want, we could provide a supervised machine learning model where the predictor / label is the rating of a game, while playtime profile and cluster label can be used as features to predict user rating. Needless to say, clustering gamers will be useful for ads-targetting as well as sale strategy.



## Get Data

For data, I am fortunate that the [HLTB website](https://www.howlongtobeat.com) exists. It allows users to log playtime and provide ratings. At the time of writing (mid Jun, 2020), the website boasts to contain data for 40k games with 200k users. This is not a lot in the big data world, however, as far as data analysis goes, this is a good start. Since the robots.txt of the website permits all scraping of publicly available data, I am free to do so. I will like to thank the www.howlongtobeat.com website for maintaining such a fantastic website and also allowing free scraping of their data.

For data ETL, I rely heavily Python [requests](https://pypi.org/project/requests/) and [bs4](https://pypi.org/project/beautifulsoup4/) packages to scrap www.howlongtobeat.com. Also important is the use of 'Inspect' developer tool on Chrome browser to reverse-engineering the source of data that I need. The tricky part is to learn how to scrap dynamically generated webpages. This requires a little AJAX knowledge, which involves sending headers and payload data in using requests.post to extract the dynamically generated html codes. I took heavy inspirations from two other github repos:  [hltb-scrapper](https://github.com/KasumiL5x/hltb-scraper) and [HowLongToBeat-PythonAPI](https://github.com/ScrappyCocco/HowLongToBeat-PythonAPI). Their codes have helped me to navigate the structures of HLTB websites, though eventually I have to write my own codes to obtain what I need. Nonetheless, I'd like to thank them for their work. For details of the codes, please refer to [documentations](docs/get_data.md).


The end results are  csv files in [data/raw](data/raw). The important ones (for next stage) are: [all_game.csv](data/raw/all_game.csv), [all_play.csv](data/raw/all_play.csv) and [all_user.csv](data/raw/all_usercsv). The [all_game.csv](data/raw/all_game.csv) file contains all information related to each such as developer and release dates. Meanwhile, the [all_user.csv](data/raw/all_user.csv) file contains all user information (including gender, age and locaitons) while the [all_play.csv](data/raw/all_play.csv) file contains user-provided gameplay information (like playtimes, ratings and platforms). The details of the data will be discussed in the next few sections.

### BEWARE: Below are work in progress

## Explore Data 
1. Create a copy for exploration
2. Study attributes and characteristics
3. Identify features and targets, as well as the type of machine learning problem(s) or modelling(s)
4. Visualize data and understand the statistics of the data. If useful, study correlations among the attributes.
4. Write down promising transformations or cleaning up to be done to do list.
5. Document the exploratory findings.

## Prepare Data 
1. Create a copy for transformation
2. Data cleaning
3. Data transformation 
4. Feature engineering and selection
5. Feature scaling

## Model Selections 
1. Shortlist a set of models, typically that means train many quick and dirty models from different categories (e.g., linear, naive, Bayes, SVM, Random Forests, neural net, etc.) using standard parameters. Do have in mind a prior which models you expect to do better than the others given the nature of the data and problems
2. Measure and compare their performance using k-fold cv
3. Study their errors
4. If needed, repeat feature selection and engineering again
5. Short-list around 3-5 promising models (incorporating various types of errors). Typically should include an ensemble model.
6. Finally, evaluat the models on test data 
(optional) Explainability of predicitons (see LIME and SHAP)

## Analytics and Insights
1. Document the findings
2. Create nice story with intuitive graphs
3. Why my solution achieves the business objective
4. Interesting talking points discovered along the way
5. Assumptions and limitations
6. What is the future use of the model? 

