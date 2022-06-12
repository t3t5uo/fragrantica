import requests
import random
import csv
import concurrent.futures

#opens a csv file of proxies and prints out the ones that work with the url in the extract function
def random_proxy():
    proxylist = []

    with open('webshare500proxies.csv', 'r') as f:
    # with open('proxyscrape_premium_proxies.csv', 'r') as f:
    # with open('proxylist.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxylist.append(row[0])
    #this was for when we took a list into the function, without conc futures.

    proxy = random.choice(proxylist)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        #change the url to https://httpbin.org/ip that doesnt block anything
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=2)
        print(r.json(), ' | new proxy')
    except:
        try:
            r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=2)
            print(r.json(), ' | new proxy')
        except Exception as e:
            print("two random proxies didn't work")
            raise
    return proxy

# proxy = extract()
# print(proxy)
