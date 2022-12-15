# Final_Project
This interactive project plans to allow users to choose some US stocks for investment and get the related information presented in an infographic manner.

## Required packages
flask
treelib
yahoo_oauth
os
requests
pandas
wikipediaapi
yfinance
peewee

## Data Source and Data Structure
Wikipedia API
Yahoo API: requires OAuth, which is in the OAuth2.json file hidden by the .gitignore file.

To create the database, wiki_cache.json, yahoo_cache.json and yahoo_tree.json are mainly used.
In yahoo_tree.json, trees are constructed from the stored data using the treelib package. Based on Industry and Sector classification, about 100 records of US stocks and their data are organized to the tree.

## Instructions to run the project
•	Download the project.
•	Make sure the listed above packages used in the project installed.
•	Run app.py file in your terminal and access the URL: http://127.0.0.1:5000.
•	Interact and submit requests in the website page.

## Interaction and Presentation
Using Flask and models, the project plans to allow users to get information of US stocks.
•	Wiki: search and find information of listed companies and other terms in the finance area.
•	Stock: search and find important data of US stocks, recent news, known holders, and cashflow graphs.
•	Kline: search and find Kline of US stocks. 











