from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import pprint

my_url = 'https://www.goodguide.com/products/420447-garnier-color-shield-shampoo-reviews-ratings#/'

def parse(my_url):
    req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})

    web_byte = urlopen(req).read()
    page_html = web_byte.decode('utf-8')

    # html parsing
    page_soup = soup(page_html, 'lxml')

parse(my_url)
print(page_soup)

# get ingredients
ingredients = []
for lists in page_soup.find_all("ul", {"class":"list product-details-ingredients"}):
    for a in lists.find_all('a'):
        ingredients.append(a.text)

# get links
links = []
for lists in page_soup.find_all("ul", {"class":"list product-details-ingredients"}):
    for a in lists.find_all('a'):
        link = a.get('href')
        links.append(link)

url = 'https://www.goodguide.com'

for link in links:
    link = url + link
print(links)
