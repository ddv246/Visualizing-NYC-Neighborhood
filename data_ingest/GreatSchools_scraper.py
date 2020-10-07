import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import re
import time

def get_page_by_num(page_num):
    url = "https://www.greatschools.org/new-york/new-york/schools/?page=" + str(page_num) + "&st%5B%5D=public_charter&st%5B%5D=public&st%5B%5D=charter&view=table"
    chrome_options = Options()  
    chrome_options.add_argument("--headless") # Opens the browser up in background
    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        html = browser.page_source
    page_soup = BeautifulSoup(html, 'html.parser')
    containers = page_soup.findAll('table')

    myhtml = str(containers[0])
    df = pd.read_html(myhtml)[0]

    all_a = containers[0].findAll('a', {'class': 'name'})
    all_addr_tags = containers[0].findAll('div', {'class': 'address'})
    ratings_tags = containers[0].findAll('span', {'class': 'tipso_style'})
    all_stars = containers[0].findAll('div', {'class': re.compile('stars')})
    all_rows = containers[0].findAll('tr')[1:]

    all_reviews = []
    for cur_row in all_rows:
        review_cell = cur_row.findAll('td')[5]
        if review_cell.contents[0] == 'No reviews yet':
            all_reviews.append(-1)
        else:
            all_reviews.append(len(review_cell.findAll('span', {'class': 'icon-star filled-star'})))

    all_ratings = []
    for cur_rating_tag in ratings_tags:
        if len(cur_rating_tag.contents[0].contents) == 0:
            all_ratings.append(-1)
        else:
            all_ratings.append(cur_rating_tag.contents[0].contents[0])


    df['Links'] = ['https://www.greatschools.org' + x['href'] for x in all_a] 
    df['Zip'] = [x.contents[0][-5:] for x in all_addr_tags]
    df['Address'] = [x.contents[0][:-7] for x in all_addr_tags]
    df['Rating'] = all_ratings
    df['Name'] = [x.contents[0] for x in all_a]
    df['UserReviewStars'] = all_reviews


    col_order = ['Name', 'Type', 'Grades', 'Address', 'Zip', 'Rating', 
                 'Total students enrolled', 'Students per teacher', 'Reviews', 'UserReviewStars', 
                 'District', 'Links']

    return df[col_order]


def get_all_pages(max_page):
    all_dfs = []
    
    for i in range(1, max_page + 1):
        print("Processing Page %s" % i)
        try:
            df = get_page_by_num(i)
            print("Found %s Results!" % df.shape[0])
            all_dfs.append(df)
            
        except:
            print("Error on Page %s" % i)
            continue
        
        # do sleep
        sleep_time = np.random.choice(range(10)) + 1
        time.sleep(sleep_time)
    
    return all_dfs
        

all_res = get_all_pages(16). # there are 16 pages total for NYC data
df_all = pd.concat(all_res)
df_all.to_csv('gs_data.csv')