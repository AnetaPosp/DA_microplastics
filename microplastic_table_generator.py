from ingredient_lists import echa_microplastics
import csv

with open('microplastics.csv','w', newline="") as microplastic_table:
  writer=csv.writer(microplastic_table)
  writer.writerow(["microplasticID","microplastic_name"])
  writer.writerows([[echa_microplastics.index(microplastic)+1, microplastic] 
                    for microplastic in echa_microplastics])