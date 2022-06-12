from selenium import webdriver
import pdb
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.proxy import Proxy, ProxyType
import get_proxy
import re
import itertools

def get_slider_percentage(element):
    max = element.get_attribute("max")
    value = element.get_attribute("value")
    percent = round((int(value) / int(max)) * 100, 4)
    return percent

def scrape_page(proxy, url):

    # options = webdriver.ChromeOptions()
    # options.add_argument('--proxy-server=' + proxy)
    # driver = webdriver.Chrome(options=options)

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument('--proxy-server=' + proxy)
    # for local
    driver = webdriver.Chrome(options=options)
    print(str(options))
    # for heroku
    # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)


    # url = "https://www.fragrantica.com/perfume/Giorgio-Armani/Acqua-di-Gio-Profumo-29727.html"
    print('getting: ' + str(url))

    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 220)")
    time.sleep(1)

    frag = {}

    icon_attributes = driver.find_elements(By.CSS_SELECTOR,'div[rating-vote="5"]')
    print(len(icon_attributes))

    comments = []
    for i, icon_attribute in enumerate(icon_attributes):

        comment = icon_attribute.find_element(By.XPATH, '../../..').text

        #remove username and time updated
        if not ':' in comment:
            comment = comment.split('ago')[-1]
        else:
            comment = comment.split(':')[-1]
            comment = comment[2:]

        #replace line breaks with spaces
        comment = comment.replace('\n', ' ').replace('\r', ' ')
        comment = comment.strip()

        #remove non-alphanumeric chars
        comment = re.sub(r'[^A-Za-z0-9 ]+', '', comment)

        # TODO 10,000 characters version
        # 3,000 characters
        if len(comment) < 500:
            if comment not in comments:
                comments.append(comment)
        if len(''.join(comments)) > 2500:
            break
        if i > 50:
            break

    full = '. '.join(comments)
    # print(full)
    # print(len(full))
    frag['comments3k'] = full

    # name = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(5) > div > p:nth-child(1) > b:nth-child(1)').text
    # print(name)
    # designer = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(5) > div > p:nth-child(1) > b:nth-child(2)').text
    # print(designer)
    # frag['designer'] = designer

    description = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(5) > div > p:nth-child(1)').text
    frag['description'] = description

    group = description.split(" is a ")[1].split(" fragrance for ")[0]
    print('group: ' + group)
    frag['group'] = group

    frag['quote'] = ''
    try:
        quote = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(5) > div > div').text
        print("quote: " + quote)
        frag['quote'] = quote
    except Exception:
        pass

    love = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(1) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('love: ' + love)
    frag['love'] = love
    like = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('like: ' + like)
    frag['like'] = like
    ok = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(3) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('ok: ' + ok)
    frag['ok'] = ok
    dislike = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(4) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('dislike: ' + dislike)
    frag['dislike'] = dislike
    hate = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(5) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('hate: ' + hate)
    frag['hate'] = hate


    winter = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(1) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('winter: ' + winter)
    frag['winter'] = winter
    spring = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(2) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('spring: ' + spring)
    frag['spring'] = spring
    summer = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(3) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('summer: ' + summer)
    frag['summer'] = summer
    fall = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(4) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('fall: ' + fall)
    frag['fall'] = fall

    day = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(5) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('day: ' + day)
    frag['day'] = day
    night = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(6) > div.voting-small-chart-size > div > div').get_attribute("style").split("width: ")[1].split("%")[0]
    # print('night: ' + night)
    frag['night'] = night

    try:
        perfumer = driver.find_element(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(3) > div.grid-x.grid-padding-x.grid-padding-y.small-up-2.medium-up-2 > div > a').text
        # print(perfumer)
        frag['perfumer'] = perfumer
    except Exception:
        pass

    frag['perfumers'] = ''
    try:
        # print('perfumers')
        perfumers_elements = driver.find_elements(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(3) > div.grid-x.grid-padding-x.grid-padding-y.small-up-2.medium-up-2 > div > a')
        perfumers_texts = [tn.text for tn in perfumers_elements]
        perfumers = ", ".join(perfumers_texts)
        # print(perfumers)
        frag['perfumers'] = perfumers
    except Exception:
        pass

    top_notes_elements = driver.find_elements(By.CSS_SELECTOR,'#pyramid > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(4) > div > div > div:nth-child(2)')
    top_notes_texts = [tn.text for tn in top_notes_elements]
    top_notes = ", ".join(top_notes_texts)
    # print(top_notes)
    frag['top_notes'] = top_notes

    middle_notes_elements = driver.find_elements(By.CSS_SELECTOR,'#pyramid > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(6) > div > div > div:nth-child(2)')
    middle_notes_texts = [mn.text for mn in middle_notes_elements]
    middle_notes = ", ".join(middle_notes_texts)
    # print(middle_notes)
    frag['middle_notes'] = middle_notes

    base_notes_elements = driver.find_elements(By.CSS_SELECTOR,'#pyramid > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(8) > div > div > div:nth-child(2)')
    base_notes_texts = [tn.text for tn in base_notes_elements]
    base_notes = ", ".join(base_notes_texts)
    # print(base_notes)
    frag['base_notes'] = base_notes


    loose_notes_elements = driver.find_elements(By.CSS_SELECTOR,'#pyramid > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(3) > div > div > div:nth-child(2)')
    loose_notes_texts = [tn.text for tn in loose_notes_elements]
    loose_notes = ", ".join(loose_notes_texts)
    # print(loose_notes)
    frag['loose_notes'] = loose_notes

    notes = list(filter(None, [top_notes, middle_notes, base_notes, loose_notes]))
    all_notes = ', '.join(notes)
    # print(all_notes)
    frag['all_notes'] = all_notes

    accords_elements = driver.find_elements(By.CSS_SELECTOR,'#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div > div')
    accords_texts = [tn.text for tn in accords_elements]
    accords = ", ".join(accords_texts)
    # print(accords)
    frag['accords'] = accords


    # PRE SLIDER TEST for longevity and gender
    # default
    # longevity '//*[@id="main-content"]/div[1]/div[1]/div/div[8]/div/div[ 5 ]/div/div[3]/div[1]/div[3]/progress'
    # gender    '//*[@id="main-content"]/div[1]/div[1]/div/div[8]/div/div[ 8 ]/div/div/div[3]/div[1]/div[3]/progress'

    # longevity default '//*[@id="main-content"]/div[1]/div[1]/div/div[ 8 ]/div/div[ 5 ]/div/div[3]/div[1]/div[3]/progress'
    # longevity 2       '//*[@id="main-content"]/div[1]/div[1]/div/div[ 8 ]/div/div[ 4 ]/div/div[3]/div[1]/div[3]/progress'
    # longevity 3       '//*[@id="main-content"]/div[1]/div[1]/div/div[ 7 ]/div/div[ 5 ]/div/div[3]/div[1]/div[3]/progress'

    # gender default    '//*[@id="main-content"]/div[1]/div[1]/div/div[ 8 ]/div/div[ 9 ]/div/div/div[3]/div[1]/div[3]/progress'
    # gender 2          '//*[@id="main-content"]/div[1]/div[1]/div/div[ 8 ]/div/div[ 8 ]/div/div/div[3]/div[1]/div[3]/progress'
    # gender 3          '//*[@id="main-content"]/div[1]/div[1]/div/div[ 7 ]/div/div[ 9 ]/div/div/div[3]/div[1]/div[3]/progress'

    longevity_child_1 = 8
    longevity_child_2 = 5
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[7]/div/div[5]/div/div[3]/div[1]/div[3]/progress'))
        longevity_child_1 = 7
    except Exception as e:
        pass
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[8]/div/div[4]/div/div[3]/div[1]/div[3]/progress'))
        longevity_child_2 = 4
    except Exception as e:
        pass
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[7]/div/div[4]/div/div[3]/div[1]/div[3]/progress'))
        longevity_child_1 = 7
        longevity_child_2 = 4
    except Exception as e:
        pass

    gender_child_1 = 8
    gender_child_2 = 9
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[7]/div/div[9]/div/div/div[3]/div[1]/div[3]/progress'))
        gender_child_1 = 7
    except Exception as e:
        pass
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[8]/div/div[8]/div/div/div[3]/div[1]/div[3]/progress'))
        gender_child_2 = 8
    except Exception as e:
        pass
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[7]/div/div[8]/div/div/div[3]/div[1]/div[3]/progress'))
        gender_child_1 = 7
        gender_child_2 = 8
    except Exception as e:
        pass
    try:
        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[7]/div/div[7]/div/div/div[3]/div[1]/div[3]/progress'))
        gender_child_1 = 7
        gender_child_2 = 7
    except Exception as e:
        pass

    try:
        frag['longevity_very_weak'] =       get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2) + ']/div/div[3]/div[1]/div[3]/progress'))
        frag['longevity_weak'] =            get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2) + ']/div/div[3]/div[2]/div[3]/progress'))
        frag['longevity_moderate'] =        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2) + ']/div/div[3]/div[3]/div[3]/progress'))
        frag['longevity_long_lasting'] =    get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2) + ']/div/div[3]/div[4]/div[3]/progress'))
        frag['longevity_eternal'] =         get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2) + ']/div/div[3]/div[5]/div[3]/progress'))

        frag['sillage_intimate'] =          get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2 + 1) + ']/div/div[3]/div[1]/div[3]/progress'))
        frag['sillage_moderate'] =          get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2 + 1) + ']/div/div[3]/div[2]/div[3]/progress'))
        frag['sillage_strong'] =            get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2 + 1) + ']/div/div[3]/div[3]/div[3]/progress'))
        frag['sillage_enormous'] =          get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(longevity_child_1) + ']/div/div[' + str(longevity_child_2 + 1) + ']/div/div[3]/div[4]/div[3]/progress'))

    except Exception as e:
        print('longevity failed')
        frag['longevity_very_weak'] = None
        frag['longevity_weak'] = None
        frag['longevity_moderate'] = None
        frag['longevity_long_lasting'] = None
        frag['longevity_eternal'] = None

        frag['sillage_intimate'] = None
        frag['sillage_moderate'] = None
        frag['sillage_strong'] = None
        frag['sillage_enormous'] = None


    try:
        frag['gender_female'] =                 get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2) + ']/div/div/div[3]/div[1]/div[3]/progress'))
        frag['gender_more_female'] =            get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2) + ']/div/div/div[3]/div[2]/div[3]/progress'))
        frag['gender_unisex'] =                 get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2) + ']/div/div/div[3]/div[3]/div[3]/progress'))
        frag['gender_more_male'] =              get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2) + ']/div/div/div[3]/div[4]/div[3]/progress'))
        frag['gender_male'] =                   get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2) + ']/div/div/div[3]/div[5]/div[3]/progress'))

        frag['price_value_way_overpriced'] =    get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2 + 1) + ']/div/div[3]/div[1]/div[3]/progress'))
        frag['price_value_overpriced'] =        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2 + 1) + ']/div/div[3]/div[2]/div[3]/progress'))
        frag['price_value_ok'] =                get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2 + 1) + ']/div/div[3]/div[3]/div[3]/progress'))
        frag['price_value_good_value'] =        get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2 + 1) + ']/div/div[3]/div[4]/div[3]/progress'))
        frag['price_value_great_value'] =       get_slider_percentage(driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div[1]/div/div[' + str(gender_child_1) + ']/div/div[' + str(gender_child_2 + 1) + ']/div/div[3]/div[5]/div[3]/progress'))

    except Exception as e:
        print('gender failed')
        frag['gender_female'] = None
        frag['gender_more_female'] = None
        frag['gender_unisex'] = None
        frag['gender_more_male'] = None
        frag['gender_male'] = None

        frag['price_value_way_overpriced'] = None
        frag['price_value_overpriced'] = None
        frag['price_value_ok'] = None
        frag['price_value_good_value'] = None
        frag['price_value_great_value'] = None
        pass

    print('scrape successful')
    driver.close()
    return frag
