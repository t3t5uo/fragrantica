from bs4 import BeautifulSoup
import requests

url = "https://www.fragrantica.com/perfume/Tom-Ford/Tobacco-Vanille-1825.html"
result = requests.get(url).text
soup = BeautifulSoup(result, "html.parser")

# tbody = soup.tbody
# trs = tbody.contents

with open("output1.html", "w") as file:
    file.write(str(soup))


print('done')
