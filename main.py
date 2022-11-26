import random
import time
import requests
import json
from bs4 import BeautifulSoup
import csv


# url = 'https://calorizator.ru/product'
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
# req = requests.get(url,headers=headers)
# src = req.text
# print(src)

# with open('index.html','w',encoding='utf') as file:
#    file.write(src)

# with open('index.html','r',encoding='utf') as file:
#     src = file.read()
# soup = BeautifulSoup(src,'lxml')
# all_products_href = soup.find(class_='product').find_all('a')
# all_categories_dict = {}
# for i in range(len(all_products_href)):
#     all_categories_dict[all_products_href[i].text] = 'http://Calorizator.ru/'+all_products_href[i].get('href')
#
# with open('all_categories_dict.json','w') as file:
#     json.dump(all_categories_dict,file,indent=4,ensure_ascii=False)

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories)) - 1
count = 0
print(f'Whole loop  {iteration_count}')
for category_name, category_href in all_categories.items():

    if ' ' in category_name:
        category_name = category_name.replace(' ', '_')

    req = requests.get(url=category_href, headers=headers)
    src = req.text
    with open(f'data/{count}_{category_name}.html', 'w', encoding="utf") as file:
        file.write(src)
    with open(f'data/{count}_{category_name}.html', encoding="utf") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    table_head = soup.find(class_="views-table sticky-enabled cols-6").find('thead').find('tr').find_all('th')
    product = table_head[1].text
    protein = table_head[2].text
    fats = table_head[3].text
    carbon = table_head[4].text
    ccal = table_head[5].text
    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';', lineterminator='\n')
        writer.writerow(
            (
                product,
                protein,
                fats,
                carbon,
                ccal
            )
        )

    products_data = soup.find(class_="views-table sticky-enabled cols-6").find('tbody').find_all('tr')
    product_info = []
    for item in products_data:
        product_tds = item.find_all('td')
        title = product_tds[1].find('a').text
        protein = product_tds[2].text
        fats = product_tds[3].text
        carbon = product_tds[4].text
        ccal = product_tds[5].text

        product_info.append({
            "Title": title,
            "Protein": protein,
            "Fats": fats,
            "Carbohydrates": carbon,
            "Calories": ccal,

        })

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(
                (
                    title,
                    protein,
                    fats,
                    carbon,
                    ccal
                )
            )
    with open(f'data/{count}_{category_name}.json,', 'a', encoding='utf-8-sig') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)
    count += 1
    print(f'code {count}.{category_name} write...')
    iteration_count = iteration_count - 1
    if iteration_count == 0:
        print('end')
        break
    print(f'else: {iteration_count}')
    #time.sleep(random.randrange(2, 4))
