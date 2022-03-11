import requests
from bs4 import BeautifulSoup

def poisci_url(niz):
    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(niz)
    content = requests.get(url).content
    soup = BeautifulSoup(content,'lxml')
    images = soup.findAll('img')
    vrni = str(images[1]).split('src="')[1].split(';')[0]
    
    
    return vrni
#     for image in images:
#         print(image.get('src'))
#     print(len(images))
#https://stackoverflow.com/questions/55787165/getting-a-url-of-some-picture-from-google-search
# a = poisci_url('messi')
# print(str(a))
