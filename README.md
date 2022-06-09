Summary: After scraping and analyzing ten most recent articles from "https://www.aljazeera.com/where/mozambique/," we find that there are 5 articles with a negative setiment, 4 with a positive sentiment and a neutral article. This data can be then used to infer the current situation in Mozambique as either positive, negative or neutral.

Documentation:
1.) We use the requests library to *send_request* to the webserver and get the raw html file.
2.) We then parse the html text using *scrape* method which in turn uses BeautifulSoup for web scraping, and build a list of ten most recent articles.
3.) We then extract meaningful data ie. title and description from the news articles using the *pre_process* method, which also uses tqdm to display progress.
4.) Now we have meaningful data which can be passed on to the setiment analysis library.
5.) The *sentiment_analysis* method then takes the processed data as input and uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to perform sentiment analysis. VADER is sensitive to both sentiment as well as intensity which is very well present in news articles, hence it becomes a suitable tool to analyze our articles. Having VADER lexicon, often considered to be the best and most up-to-date human verified sentiment lexicons gives us accurate results. Also, VADER provides us with a normalized score which helps us easily categorize news articles. Hence, VADER is the most optimal choice for classifying our articles.
6.) The compound sentiment polarity is analyzed to categorize the sentiment of the articles and is added back as a dict key in the article dictionary.
7.) This analyzed data is then plotted(*u_plot*) using plotly and pandas, this gives us a clear count of the distribution of the articles accross different sentiments. Looking at the graph gives us the overall trend of articles being analyzed.

How to run (Ubuntu):
0.) Install Python-3.8+ on your local test bed.
1.) Create a virtual environment - "python3 -m venv env"
2.) Activate the environment - source env/bin/activate
3.) Install requirements.txt - pip3 install -r requirements.txt
4.) Run the python script - python3 scrape_and_plot.py
5.) Plot will open in browser

Total time of execution - 0.75seconds

Note: data.json contains the title and description of each news article for which sentiment has been computed. JSON stands for JavaScript Object Notation, it is lightweight and used for data transportation. Having data in this format will help us to provide REST APIs easily.