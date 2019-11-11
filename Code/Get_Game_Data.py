from selenium import webdriver as wd
# from selenium.webdriver.support.ui import Select
import selenium
import time
import pandas as pd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



path = "../Raw CSV/"
url_vals = pd.read_csv('../game urls.csv')
url_list = url_vals["url"].tolist()

headless = True
browser = get_browser()
start = 0
###
##
def sleep(sec = 4):
    time.sleep(sec)
#
def get_browser():
    chrome_options = wd.ChromeOptions()
    if headless == True:
    	chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(options=chrome_options)
    return browser


#Gets the game title
def get_game_title():
    title = browser.find_element_by_class_name("app-description__title").get_attribute("innerHTML")
    return title
#Exctrac price
def get_game_price():
    price = browser.find_element_by_class_name("app-purchase-price").find_element_by_css_selector("span").get_attribute("innerHTML")
    return price
#Excract number of reviews
def get_review_count():
    review_count = browser.find_element_by_class_name("app-description__review-count").text
    review_count = review_count.replace(" Ratings", "")
    return review_count
#Extract percent of 5,4,3,2,1 stars
def get_review_scores():
    review_scores = browser.find_element_by_class_name("app-ratings-histogram").text
    scores = review_scores.split("\n") 
    stars = [scores[i] for i in range(0,len(scores),2)]
    percent = [scores[i] for i in range(1,len(scores),2)]
    return({"stars":stars, "percent":percent})

#Get esrb
def get_esrb():
    esrb_age= browser.find_element_by_class_name("app-age-rating-icon__text").text
    return esrb_age
#Returns short game description
def get_game_description():
    game_description_text = browser.find_element_by_class_name("store-item-detail-page-description__content").text
    return game_description_text
#Returns other details    
def get_additional_details():
    details = browser.find_element_by_class_name("app-details").text
    detail_list = details.split("\n")[1:]
    keys = [detail_list[i] for i in range(0, len(detail_list),2)]
    vals = [detail_list[i] for i in range(1, len(detail_list),2)]
    return{"keys":keys, "vals":vals}

#Add additional definitions here for what you want to extract


#Gets all data
def get_data(url):
    #Will fail for early access games
    try:
        browser.get(url)
        sleep()
        title = get_game_title()
        price = get_game_price()
        num_reviews = get_review_count()
        esrb = get_esrb()
        description = get_game_description()
        #
        review_scores = get_review_scores()
        review_star_names = review_scores["stars"]
        review_star_percent = review_scores["percent"]
        additional_details = get_additional_details()
        additional_detail_keys = additional_details["keys"]
        additional_detail_vals = additional_details["vals"]
        values_list = [title, url,price, num_reviews, esrb, description] + review_star_percent + additional_detail_vals 
        col_names = ["title", "url", "price", "num_reviews", "esrb", "description"] + review_star_names + additional_detail_keys 
        df = pd.DataFrame(dict(zip(col_names, values_list)), index = [0])
        return df
    except:
        print(f"Url {url} Failed")
        return pd.DataFrame()

    # print(len(col_names))
    # print(len(values_list))
   

#Runs through url list and creates a csv for each which is saved to the path folder (create path folder)
def get_multiple_game_data(url_list, path, start):
    failed_list = []
    failed_list_num = []
    for i in range(start, len(url_list)):
        print(f"Currently loading data from {i+1}")
        data = get_data(url_list[i])
        if data.empty == False:
            data.to_csv(path + "game_data_"+str(i+1)+".csv")
        else:
            failed_list.append(url_list[i])
            failed_list_num.append(i+1)
    return pd.DataFrame({"number":failed_list_num,"url":failed_list})
		        


failed = get_multiple_game_data(url_list, path, start)
failed.to_csv("../Failed.csv")
print("done")