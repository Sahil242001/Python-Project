# Sahil Patel 
# munews_rss.py - Generate a RSS feed Xml file from the first two pages of articles at the MU news site (https://www.monmouth.edu/news/archives and https://www.monmouth.edu/news/archives/page/2/). 
#               - Script must retrieve the news pages using the requests module.
#               - Then parse the individual headlines as well as the corresponding links to be included in the output XML file.
#               - Scrpit must also parse the publication date of each article from the <pubDate> RSS element.
import requests
import bs4
import PyRSS2Gen
import datetime


url = requests.get('http://www.monmouth.edu/news/archives') 
another_url = requests.get('https://www.monmouth.edu/news/archives/page/2/')

html = url.text
another_html = another_url.text

munews = bs4.BeautifulSoup(html, "html.parser")

another_munews = bs4.BeautifulSoup(another_html, "html.parser")

articles = munews.select('article')
another_article = another_munews.select('article')

# Getting all the titles.
titles = []
for article in articles:
    titles.append(article['aria-label'])

# Getting all the links.
links = []
for article in articles:
    anchor = article.find('a')
    links.append(anchor['href'])

# Using a list comprehension to create newsfeed:
newsfeed = dict( [ (titles[i], links[i]) for i in range(len(titles) ) ] )

# Empty descriptions
descriptions = []
descriptions.append(" ")

# Constructing RSS object
rss = PyRSS2Gen.RSS2(
    title = "MU News Feed First Page", 
    link = "http://www.monmouth.edu/news/archives", 
    description = " ",
    lastBuildDate = datetime.datetime.now(),
    items = [
        PyRSS2Gen.RSSItem(
            title = "MU News Feed Second Page",
            link = "https://www.monmouth.edu/news/archives/page/2/",
            description = " ",
        )
    ]
)

# Populating items list
for i in range(len(titles)):
    rss.items.append(PyRSS2Gen.RSSItem(title = titles[i],
                                       link = links[i]))
rss.write_xml(open("munews_rss.xml", "w"))

