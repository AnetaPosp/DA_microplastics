# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:44:25 2020

@author: Aneta
"""
import urllib.request
from bs4 import BeautifulSoup

#níže manuálně vyhledané linky na katalog produktů z dané kategorie
pletova="https://www.tetadrogerie.cz/eshop/produkty/pletova-kosmetika?stranka=9&pocet=60"
telova="https://www.tetadrogerie.cz/eshop/produkty/telova-kosmetika?stranka=18&pocet=60"
vlasova="https://www.tetadrogerie.cz/eshop/produkty/vlasova-pece?stranka=19&pocet=60"
krasa_a_parfemy="https://www.tetadrogerie.cz/eshop/produkty/krasa-a-parfemy?stranka=28&pocet=60"
parfemy="https://www.tetadrogerie.cz/eshop/produkty/krasa-a-parfemy/parfemy?stranka=4&pocet=60"
zuby_a_usta="https://www.tetadrogerie.cz/eshop/produkty/hygiena/pece-o-zuby?stranka=7&pocet=60"
lubrikanty="https://www.tetadrogerie.cz/eshop/vysledky-vyhledavani?searchtext=lubrika%C4%8Dn%C3%AD"
intimni="https://www.tetadrogerie.cz/eshop/produkty/hygiena/damska-hygiena/intimni-hygiena"
panska="https://www.tetadrogerie.cz/eshop/produkty/pansky-svet?stranka=9&pocet=60"
na_cesty="https://www.tetadrogerie.cz/eshop/produkty/hygiena/hygiena-na-cesty"


def find_links(url):
    """
    otevře stránku, v html kodu najde odkazy na všechny zobrazené produkty
    vrací list s odkazy
    """
    r=urllib.request.urlopen(url).read()
    b=BeautifulSoup(r,"html.parser")
    l=b.find_all("div",class_="sx-item j-ajax-content j-item")
    links=[]
    for item in l:
        link="https://www.tetadrogerie.cz"+str(item.a["href"])
        #    print(link)
        links.append(link)
    return links

for item in [pletova, telova, vlasova, krasa_a_parfemy, parfemy, zuby_a_usta, lubrikanty, intimni,panska,na_cesty]:
    print(find_links(item))
    print("")

