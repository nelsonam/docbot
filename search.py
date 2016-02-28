import urllib
import requests
from bs4 import BeautifulSoup


def search_docs(searchquery):
    query = searchquery
    alpine = "https://alpine.atlassian.net"
    base_url = "https://alpine.atlassian.net/wiki/dosearchsite.action?queryString="

    url = base_url+urllib.quote_plus(query)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    results = []
    # get all the search results on the first page
    for link in soup.find_all("a", class_="search-result-link"):
        # get the links
        page = link.get('href')
        # get the titles
        title = link.get_text()
        # filter out old doc versions
        if 'CD/' not in page and 'DOC/' not in page:
            results.append(title)
            results.append(alpine+page)
    return results
