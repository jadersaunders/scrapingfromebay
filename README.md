# Project 3: Scraping From eBay

Instructions for this project can be found [here](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03)

My `ebay-dl.py` file converts ebay's html files into `.json` or `.csv` files.  These files display the name (`name`), price (`price`), status (`status`) and shipping price (`shipping`) of the item.  They also show whether free returns (`free_returns`) are available for the item, in addition to the number of items sold (`items_sold`) per item. 

In order to run the python file and generate json files, use the following command: 
```
$ python3 ebay-dl.py 'ant traps' 
```

The key term 'ant trap' is interchangeable with any search term.  I also downloaded files with the search terms 'sunglasses' and 'goggles'.  Note that the search term must be placed in quotations if there is a space between words.  The program is set to download 10 pages if no page count is specified, but if more/fewer pages are being downloaded, the command can be adjusted as follows (8 pages would be printed based on the command below): 

```
$ python3 ebay-dl.py 'ant traps' --num_pages=8 
```

The program runs with `.json` files by default.  In order to run the python file and generate csv files `.csv`, use the following command and add `--csv=True`: 

```
$ python3 ebay-dl.py 'ant traps' --csv=True
```


