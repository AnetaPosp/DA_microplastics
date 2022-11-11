The pages with the entire assortment in the given category were manually searched,
and the link to it was saved in link_finder.py (appendix 4.6). The script written
in link_finder contains the find_links function, which opened each link, found all
links to the pages of individual products, and appended them to the list. The
obtained lists were saved in links.py (for its lenght not shown in printed version;
available online in Appendix II). For the purpose of archiving and possibility of
offline work, the pages with product information were downloaded and saved in text
files by downloader.py (appendix 4.7). It contains DownloadPage function, that
opens the link to individual product, finds product’s name and saves the html code
to a file with product’s name. It also includes a command to print the product
name to the console and a short stop, and basic error handling for skipping unsaved
or non-existent files. This allowed control of downloading entire categories, which
were downloaded by simple for loops listed below in the downloader.py. E.g. When
downloading the "hair care" category, some non-cosmetic items such as clippers or
hair bands also appeared among cosmetic products. The download delay made
it possible to monitor what was being downloaded while manually deleting noncosmetic
products. In this manner, information about total of 2478 products was
downloaded.
Another goal was to find and sort key data for each product. This was done by
the analyzer.py file (appendix 4.8), which includes the analyze_products function.
It opens text files with stored html codes, parses them and searches for the required
information. Based on this, it creates objects of type "Product". The attributes
of these objects are the product name, its price, category, subcategory and subsubcategory,
and composition, with the composition being divided into six groups
by the categorize_ingredients function. Groups are microplastics, other synthetic
polymers, polyethers, degradable ingredients, minerals and others.
The division of ingredients into these groups was semi-automatic, as a sufficiently
large and freely available database of cosmetic ingredients and their nature was not
found. For microplastics, ECHA’s list of polymers that are considered microplastics
[129] was used. It contains 19 polymer groups, each including many different compounds 
with different INCI names. Other ingredients were initially sorted only by
short lists stored in ingredient_lists.py, and by simple logic - if the ingredient name
is "extract" or "juice", it can be assumed that it will be a biobased and biodegradable
ingredient. "ci" in turn means pigments that generally do not belong to microplastics.
Nevertheless, automatic decision about most ingredients was not possible at
first. Therefore, when categorize_ingredient function encountered an unknown ingredient,
it asked the user (ie me) to which group the ingredient belonged. I decided
it either on the basis of existing knowledge or according to information available
online. The function stored the information for further use. Therefore, the lists of
categorized ingredients grew and necessity for manual labor gradually decreased. At
the end, all ingredients were categorized, and lists with individual ingredient groups
were stored in the updated version of ingredient_lists.py (for its lenght not attached
to printed version; available online in Appendix II).
After going through all the products in a given category, the analyze_products
function generates a short report on the number of analyzed products in the given
product category, and on the occurrence of synthetic polymers in them. This was
done for all categories. The whole report is given in the 4.10 appendix. Furthermore,
the analyze_products function returns a list of lists with product attributes,
together with a table of productID - microplasticID relations. These data are useful
for constructing .csv files as sources for a visualization software. Another .csv with
microplasticID - microplastic_name assignment was constructed using microplastic_
table_generator.py file (appendix 4.9).
The data were visualized in PowerBI Desktop. The model connecting the three
tables is given in fig. 4.29. The whole interactive dashboard can be found on
https://app.powerbi.com/links/xY92HUv_K2?ctid=c63ce729-ca17-4e52-aa2d-96b
79489a542&pbi_source=linkShare. A brief overview is in fig. 4.30. As can be seen,
microplastics are quite widely used, especially in decorative cosmetics. At the same
time, products from this category most often contain more than one ingredient from
the category of microplastics. Some mascaras and lipsticks contained up to five
microplastic species. Other categories rich in microplastics were skin and hair care.
The most used microplastics were acrylate and methacrylate copolymers, which
appeared in products from all categories. This class is very wide in terms of physical
and chemical properties of the polymers, performing a wide range of functions, from
thickening and film-forming to enhancing sensory properties. Silicone polymers were
the second most popular group of microplastics, finding use mainly in decorative,
skin and hair care. Their main role is enhancement of sensorial properties, such as
skin feel or slipperiness and shine of hair. Polyamides were the third most popular
ones, finding use in decorative and skin care. Polyamides are solids that do not
dissolve in water or common cosmetic oils, alike PHB. Therefore, it seems that PHB 
could find application in the same segments. In their microparticulate form,
polyamides serve as sensory enhancers, rheology modifiers and "soft focus" agents in
high-end products.
