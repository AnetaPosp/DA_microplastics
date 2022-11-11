# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:08:11 2020

@author: Aneta
"""

import urllib.request
from bs4 import BeautifulSoup
import random
import time
import links

def DownloadPage(url):
    """
    pro stahování infa o kosmetice z eshopu Teta drogerie
    html ukládá do texťáku ve složce cosmetics
    """
    html=BeautifulSoup(urllib.request.urlopen(url).read(),"html.parser")
    name=(html.find("a",class_="j-scroll-to-target").string).strip()
    textfile="cosmetics/"+name+".txt"
    
    try:
        with open(textfile,"w") as notebook:
            notebook.write(str(html))
        print("finished: "+name)
    except UnicodeEncodeError:
        print("error")
    except FileNotFoundError:
        print("notfounderror")
    
    time.sleep(random.random())
    
# for link in links.pletova:
#     DownloadPage(link)
    
# for link in links.telova:
#     DownloadPage(link)
    
# for link in links.vlasova:
#     DownloadPage(link)
    
# for link in links.krasa_a_parfemy:
#     DownloadPage(link)
    
# for link in links.parfemy:
#     DownloadPage(link)
    
# for link in links.zuby_a_usta:
#     DownloadPage(link)    
    
# for link in links.lubrikanty:
#     DownloadPage(link)  
    
# for link in links.intimni:
#     DownloadPage(link)
    
# for link in links.panska:
#     DownloadPage(link)
    
for link in links.na_cesty:
    DownloadPage(link)

"""
stahování po kategoriích se dělalo postupně, aby se stíhalo manuální
dotřídění souborů. Např. jsem ze stažených odstranila věci, co nejsou 
kosmetika - kartáče, pilníky, vlhčené ubrousky apod. 
"""
