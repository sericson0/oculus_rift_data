import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
##
from selenium import webdriver as wd
import selenium
import time
import pandas as pd
##_____________________________________________________________
##_____________________________________________________________
##_____________________________________________________________
#Website url
url = "https://www.oculus.com/experiences/rift/section/1736210353282450/#/?_k=k8yv60"
#Sleep simply pauses for 5 seconds. Useful for letting website run javascript
# set to more than 75 if you need more games
num_scrolls = 75
headless = True
##______________________________________________________________
def sleep(sec = 5):
    time.sleep(sec)

#Tells selenium to create a browser
def get_browser():
    chrome_options = wd.ChromeOptions()
    if headless == True:
    	chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(options=chrome_options)
    return browser



def get_game_urls(sleep_sec = 5, counter_break = 100):
    #Gets urls for each game visible on page
    #could probably speed up code by setting sleep_sec to less than 5. 
    #Maybe play around with it if you need lots and lots of games.
    sleep(sleep_sec)
    game_list = []
    counter = 1
    #Selector to get all games
    games = browser.find_elements_by_class_name("store-section-item")
    for game in games:
        #Grab url of game website
        game_list.append(game.find_element_by_css_selector("a").get_attribute("href"))
        #For printing how the scraper is doing
        if counter % counter_break == 0:
            print(counter)
        counter += 1
    return game_list


def scroll_page():
    #Scrolls down the page
    try:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        return True
    except:
        return False



browser = get_browser()
browser.get(url)
print("starting to get initial games")

game_url_list = []

# if start_scroll_pos > 0:
#     for i in range(start_scroll_pos):
#         print(f"scrolling to {i+1}")
#         sleep()
#         scroll_page()



# for i in range(num_scrolls):
#     print(f"Current Scroll {i+1}, current length of url list {len(game_url_list)}")
#     game_url_list += copy.deepcopy(get_game_urls())
#     scroll_result = scroll_page()
#     if scroll_result == False:
#         print("End of scrolling")
#         break
for i in range(num_scrolls):
    #Scroll down a bunch to load a bunch of games
    print(f"scrolling to {i+1}")
    sleep(4)
    scroll_result = scroll_page()
    if scroll_result == False:
        print("End of scrolling")
        break

print("scraping files")
game_url_list = get_game_urls()
print(f"scraped {len(game_url_list)} urls")

# print(game_url_list)
# df = pd.DataFrame(list(set(game_url_list))) #The list set thing removes duplicates
df = pd.DataFrame(game_url_list, columns = ["url"]) #The list set thing removes duplicates
df.to_csv("../game urls.csv")
print("Code is done running")
