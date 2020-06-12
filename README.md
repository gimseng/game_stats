# game_stats

Welcome to my gameplay data analysis project (which I call game_stats). In this project, we will be doing an end-to-end data science project, involving perhas a few data engineering/machine learning modeling task. I am structuring the project in the following ways.

## ## Strategy, Big Picture/Project Motivation, Problem Statement and Project Goals
1. Define the business objectives and gameplans.
2. How will my solution be used?
3. Current solution?
4. Performance measure? 
5. Assumptions?

## Get Data
1. Legality and permission?
2. Extract, transform and load (ETL)
3. If needed, build database and pipeline/API access for later steps.

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

