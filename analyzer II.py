# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:35:44 2020

@author: Aneta
"""

from bs4 import BeautifulSoup
import os
import csv
from ingredient_lists import echa_microplastics, other_synthetic_polymer, polyether, mineral, readily_degradable, other
from brands import brand_list

class Product(object):
    def __init__(self,ID,name,price,category, subcategory, subsubcategory, ingredients):
        """
        předpokládá, že v textu se seznamem ingrediencí jsou jednotlivé složky oddělené čárkami
        rozseká ingredients na jednotlivé složky a hodí je do listu, a roztřídí
        """
        self.ID=ID
        self.name=name
        self.add_brand()
        self.price=price
        self.category=category
        self.subcategory=subcategory
        self.subsubcategory=subsubcategory
        self.ingredients=ingredients
        self.ingredient_list=[i.lower().strip() for i in ingredients.split(",")]
        self.categorize_ingredients()

    def add_brand(self):
      global brand_list
      possible_brands=[brand for brand in brand_list if brand in self.name]
      if len(possible_brands)==1:
        self.brand=possible_brands[0]
      elif len(possible_brands)==2:
        possible_brands.remove("Palette ") #neb nejčastější kiks je, že Palette v názvu není značka, ale slovo
        self.brand=possible_brands[0]
      else:
        self.brand = self.name.split()[0] #pokud není značka v seznamu, vzít jako značku první slovo názvu. Podle printu zkontrolovat
    
    def categorize_ingredients(self):
        """
        podívá se, jaké jsou v produktu ingredience, a zda jsou v některém seznamu známých složek
        pokud ano, zařadí ingredienci do příslušné kategorie
        pokud ne, zkusí to sám dovodit z názvu
        při nejhorším se zeptá uživatele, co to je. podle toho to zařadí a navíc zapíše do seznamu známých složek
        """
        global echa_microplastics
        global other_synthetic_polymer
        global polyether
        global readily_degradable
        global other
        global mineral
        self.microplastics=[]
        self.syntpolymers=[]
        self.degradable_ings=[]
        self.uncategorized=[]
        self.minerals=[]
        self.polyethers=[]
        for ingredient in self.ingredient_list:
            if ingredient in echa_microplastics:
                self.microplastics.append(ingredient)
            elif ingredient in other_synthetic_polymer:
                self.syntpolymers.append(ingredient)
            elif ingredient in polyether:
                self.polyethers.append(ingredient)
            elif ingredient in readily_degradable:
                self.degradable_ings.append(ingredient)
            elif ingredient in other:
                self.uncategorized.append(ingredient)
            elif ingredient in mineral:
                self.minerals.append(ingredient)
            elif "extract" in ingredient or "juice" in ingredient: #zavádím předpoklad, že rostlinné extrakty jsou rozložitelné
                self.degradable_ings.append(ingredient)
                readily_degradable.append(ingredient)
            elif "ci " in ingredient: #zde předpoklad, že barvy patří do 'other'
                self.uncategorized.append(ingredient)
                other.append(ingredient)
            else:
                self.ask(ingredient)
                
    def ask(self,ingredient):
        """
        zeptá se uživatle, kam zaředit neznámou surovinu. Podle toho ji zařadí produktu
        a připíše do příslušného listu známých surovin
        """
        global echa_microplastics
        global other_synthetic_polymer
        global polyether
        global readily_degradable
        global other
        global mineral
        i=str(input("kam patří "+ingredient+"? (echa mikroplast:e, synt. polymer:s, polyether: p, minerál:m, degradovatelné:d, jiné: o): "))
        if i=="e":
            echa_microplastics.append(ingredient)
            self.microplastics.append(ingredient)
        elif i=="s":
            other_synthetic_polymer.append(ingredient)
            self.syntpolymers.append(ingredient)
        elif i=="d":
            readily_degradable.append(ingredient)
            self.degradable_ings.append(ingredient)
        elif i=="m":
            mineral.append(ingredient)
            self.minerals.append(ingredient)
        elif i=="o":
            other.append(ingredient)
            self.uncategorized.append(ingredient) 
        elif i=="p":
            polyether.append(ingredient)
            self.polyethers.append(ingredient)
        else:
            self.ask(ingredient)
            
    def __str__(self):
        print("-------")
        print("ID:"+str(self.ID))
        print(self.name)
        print("  "+self.category)
        print("  "+str(self.price)+" Kč")
        print("   ")
        print("složení: "+self.ingredients)
        print("   ")
        print("mikroplasty: "+str(self.microplastics))
        print("syntetické polymery: "+str(self.syntpolymers))
        print("polyethery: "+str(self.polyethers))
        print("degradovatelné složky: "+str(self.degradable_ings))
        print("minerální složky: "+str(self.minerals))
        return "jiné: "+str(self.uncategorized)

    def list_attributes(self):
        return [self.ID,
        self.name,
        self.brand,
        self.category, 
        self.subcategory,
        self.subsubcategory,
        self.price,
        self.ingredients,
        len(self.microplastics),
        self.microplastics]

    def list_fact_table(self):
      global echa_microplastics
      if self.microplastics:
        return [[self.ID, echa_microplastics.index(microplastic)+1] for microplastic in self.microplastics]
      else:
        return [[self.ID, 0]]

def analyze_products(categ):
    """

    Parameters
    ----------
    categ : str, musí se shodovat s názvem složky v cosmetics
    
    vyhledá složku s některou kategorií produktů, pootvírá soubory
    z každého souboru s infem o produktu vycucne název, cenu, ingredience
    vytvoří objekt Product
    pokud obsahuje syntetické polymery, zapíšou se
    vypíše se krátký report

    Returns
    -------
    list listů se seznamy atributů pro jednotlivé produkty

    """
    global ID 

    folderPath = 'cosmetics/'+categ
    products=[]
    with_microplastics=0
    with_other_synt_polymers=0   
    analyzed_products=0
    all_microplastics=[]
    errors=[]
    facts=[]
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            path="cosmetics/"+categ+"/"+str(file)
            with open(path) as item:
                b=BeautifulSoup(item.read(),"html.parser")
                # print(b.prettify())
                name=str(file).rstrip(".txt")
                # print(name)
                category_list =[text.strip() for text in b.find("div", class_ = "sx-breadcrumbs").strings if text.strip()]
                cat, subcat = category_list[2:4]
                if len(category_list) > 5:
                  subsubcat = category_list[4]
                else:
                  subsubcat = ""
                price_list=[text for text in b.find("div",class_='sx-item-price-group').strings] 
                #dává [koruny,halíře,akční cena koruny, akční cena halíře, \n]
                # print(price_list)
                try:
                    price=float(price_list[0]+"."+price_list[1]) #sečte koruny s halířema a zapíše neakční cenu
                except ValueError: #úprava cen nad tisícovku (1 299,90)
                    #print(name)
                    #print(price_list)
                    if "'>" in price_list[0]:
                        price=float("".join([item.strip() for item in (price_list[1]).split()])+"."+price_list[2])
                        #print(price)
                    else:
                        errors.append(str(file))
                try:
                    ings=b.find("div",id="slozenialergeny").p.string
                    #print(ings)
                    p=Product(ID,name,price,cat, subcat, subsubcat,ings)
                    analyzed_products+=1
                    # print(p)
                    products.append(p.list_attributes())
                    facts+=p.list_fact_table()
                    if p.syntpolymers!=[]:
                        with_other_synt_polymers+=1
                    if p.microplastics!=[]:
                        with_microplastics+=1
                    ID+=1
                except AttributeError:
                    errors.append(path)  

                
    print("kategorie: "+categ)
    print("analyzovaných produktů: "+str(analyzed_products))
    print("s mikroplasty: "+str(with_microplastics))
    print("s jinými syntetickými polymery: "+str(with_other_synt_polymers))
    print("mikroplasty v kategorii: ")
    for polymer in echa_microplastics:
        c=all_microplastics.count(polymer)
        if c>0:
            print("   "+polymer+":"+str(c)+"x")
    print("")
    
    return products, facts

ID = 1
with open('products.csv', 'w', newline="") as products, open('products_microplastics.csv', 'w', newline = "") as fact_table:
  product_writer = csv.writer(products)
  fact_writer = csv.writer(fact_table)
  product_writer.writerow(["ID","name","brand","category","subcategory","subsubcategory","price",
                           "ingredients","no_microplastics","microplastics"])
  fact_writer.writerow(["productID","microplasticID"])
  for category in ["cestovni","dekorativni","intimni","lubrikanty","panska","parfemy_a_deodoranty",
                   "pletova","telova","vlasova","zuby_a_usta"]:
    result=analyze_products(category)
    product_writer.writerows(result[0])
    fact_writer.writerows(result[1])