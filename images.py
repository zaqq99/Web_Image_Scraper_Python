import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json as js
import os


def Start_Search():

    # Parametry
    url = "https://www.bing.com/images/search"
    search = input("What are u looking for? ")
    params = {"q": search}

    # Nazwa katalogu
    dir_name = search.replace(" ", "_").lower()

    # Jeśli nie ma takiego katalogu, to go stwórz
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    # Request i Soup
    r = requests.get(url, params)
    soup = BeautifulSoup(r.text, "html.parser")

    # Wyszukiwanie elementów html a, który ma klasę: iusc
    links = soup.findAll("a", {"class": "iusc"})

    # Wyświetlenie rezultatów
    print("Results:", len(links))

    # Pętla która przechodzi przez każdy link ze znalezionych elementów
    for link in links:
        try:
            # Uzyskujemy własność z danego linku, ta własność to odnośnik do wyszukanego obrazu
            m = js.loads(link.attrs['m'])
            murl = m['murl']
            name = murl.split('/')[-1]
            r = requests.get(url=murl)
            try:
                # Zapisywanie zdjęcia
                img = Image.open(BytesIO(r.content))
                img.save("./" + dir_name + "/" + name, img.format)
                print("Image:", murl)
            except:
                print('Could not save image.')
        except:
            print('Could not save image.')

    Start_Search()


Start_Search()
