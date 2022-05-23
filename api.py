from flask import Flask
import requests, wikipedia
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'homepage'

def getdata(url):
    r = requests.get(url)
    return r.text

@app.route('/<name>', methods=['get', 'post'])
def url(name):
    wiki=wikipedia.search(name)     # search wikipedia for name
    results={}
    page=None

    for term in wiki:
        results[term.lower()]=term  # populate results with {cvs caremark: CVS Caremark...}

    # create url with error handling
    try:
        if name in results:
            page=wikipedia.page(results[name], auto_suggest=False).url
        else:
            if ' ' in name:
                name=name.title()
            page="https://en.wikipedia.org/wiki/%s" %name
    except wikipedia.exceptions.DisambiguationError:
        return 'DisambiguationError: query too broad, please be more specific in your search term'

    htmldata = getdata(page)
    soup = BeautifulSoup(htmldata, 'html.parser')
    images = soup.select('table.infobox a.image img[src]')

    return 'http:'+images[0]['src']


if __name__ == '__main__':
   app.run(debug=True)