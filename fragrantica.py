# from selenium import webdriver
# import pdb
# import time
# from selenium.webdriver.common.by import By
#
# driver = webdriver.Chrome()
#
# driver.get("https://www.fragrantica.com/search/")
# time.sleep(5)
#
# # driver.find_element_by_css_selector('#main-content > div.grid-x.grid-margin-x > div.small-12.medium-8.large-9.cell > div > div > div > div.off-canvas-content.content1.has-reveal-left > div.grid-x.grid-padding-x.grid-padding-y > div > div:nth-child(3) > div > div > div > div > div > button').click()
#
# # print(driver.find_elements_by_xpath("//*[contains(text(), 'Show more results')]"))
#
# driver.find_elements_by_xpath("//*[contains(text(), 'Show more results')]")[-1].click()
# driver.find_elements_by_xpath("//*[contains(text(), 'Show more results')]")[-1].click()
# driver.find_elements_by_xpath("//*[contains(text(), 'Show more results')]")[-1].click()
# driver.find_elements_by_xpath("//*[contains(text(), 'Show more results')]")[-1].click()
#
#
#
#
#
#
#
# driver.close()

import re,requests
from simplified_scrapy.simplified_doc import SimplifiedDoc
import html

with open('/home/alex/Downloads/view-source_https___www.fragrantica.com_search_.html', "r") as f:
    page = f.read()
source_code = html.parse(page)

# source_code = requests.get('https://stackoverflow.com/')

doc = SimplifiedDoc(source_code.content.decode('utf-8')) # incoming HTML string
lst = doc.listA(url='https://stackoverflow.com/') # get all links
for a in lst:
  if(a['url'].find('stackoverflow.com')>0): #sub domains
    print (a['url'])
