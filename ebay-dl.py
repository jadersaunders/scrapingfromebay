import argparse 
import json 
import csv 
from ctypes.wintypes import tagSIZE
from fileinput import filename 
import requests
from bs4 import BeautifulSoup 

def parseprice(tag):
    numbers = ''
    if '$' not in tag: 
        return 0 
    if ' ' in tag: 
        j=tag.split()
        tag = j[0]
    for c in tag: 
        if c in '1234567890':
            number+=c
    return int(numbers)

def parseshipping(text):
    numbers = ''
    for c in text: 
        if 'free' in text.lower():
            return 0
        elif c in '1234567890':
            numbers += c 
    return int(numbers)

def parseitems_sold(text):
    numbers = ''
    for c in text: 
        if c in '1234567890':
            numbers += c 
    if 'sold' in text: 
        return int(numbers)
    else: 
        return 0

if __name__=='__main__': 

    parser = argparse.ArgumentParser(description='download ebay information and convert to json')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', default=False)
    args = parser.parse_args()

print('args.search_terms=', args.search_term)

# all ebay items list 
items = []

# loop over ebay webpages 
for pagenumber in range(1,int(args.num_pages)+1):

    # build the url 
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn=' + str(pagenumber)

    # download html 
    r = requests.get(url)
    status = r.status_code 
    html = r.text 

    # processing html 
    soup = BeautifulSoup(html, 'html.parser')

    # loop items in page 
    tagsitems = soup.select('.s-item')
    for tagitem in tagsitems: 

        name = None 
        tagsname = tagitem.select('.s-item__title')
        for tag in tagsname: 
            name = tag.text 

        price = None 
        tagsprice = tagitem.select('.s-item__price')
        for tag in tagsprice: 
            price = parseprice(tag)

        status = None 
        tagsstatus = tagitem.select('.SECONDARY_INFO')
        for tag in tagsstatus: 
            status = tag.text

        shipping = None 
        tagsshipping = tagitem.select('.s-item__shipping, .s-item__freeXDays')
        for tag in tagsshipping: 
            shipping = parseshipping(tag.text)

        free_returns = False
        tagsfreereturn = tagitem.select('.s-item__free_returns')
        for tag in tagsfreereturn: 
            free_returns = True 

        items_sold = None
        tagsitems_sold = tagitem.select('.s-item__hotness, .s-item__additionalItemHotness')
        for tag in tagsitems_sold: 
                items_sold = parseitems_sold(tag.text)

        item = {
            'name': name, 
            'price': price, 
            'status': status, 
            'shipping': shipping, 
            'free_returns': free_returns, 
            'items_sold': items_sold
        }
        items.append(item)


if bool(args.csv) == True: 
    csv_columns = ['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold']
    filenamecsv = args.search_term+'.csv'
    filenamecsv = filenamecsv.replace(" ", "_")
    with open(filenamecsv, 'w', newline='', encoding='utf-8') as f: 
        ebaywritercsv = csv.DictWriter(f, fieldnames=csv_columns)
        ebaywritercsv.writeheader()
        for item in items: 
                ebaywritercsv.writerow(item)

# json file 
else:
    filename = args.search_term +'.json'
    filename = filename.replace(" ", "_")
    with open(filename, 'w', encoding='utf-8') as t:
        t.write(json.dumps(items))


# to use the CSV flag: set --csv=True (add at end after --num_pages=1)
# to use the JSON flag: add 'searchterm' --num_pages=1 for specific page numbers, otherwise default = 10 