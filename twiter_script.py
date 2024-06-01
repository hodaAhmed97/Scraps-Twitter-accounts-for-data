from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import time

    
word = "$TSLA"

def scroll_to_next_tweet(driver):
    tweet_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    last_tweet = tweet_elements[-1]
    last_tweet_location_y = last_tweet.location['y']
    driver.execute_script(f"window.scrollTo(0, {last_tweet_location_y});")
    time.sleep(5)  # Adjust sleep time as needed

def app(listofurls, ticker ,interval):
    start_time = time.time()

    total_occur = 0 

    for url in listofurls:
        start_time_for_this_url = time.time()
        occur_for_this_url = 0
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        # Let the page load
        time.sleep(10)
        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')


        alltweets = {}
        for tweet in tweets: 
            alltweets[tweet.text] = 1
        while True:
            oldsize = len(alltweets)
            scroll_to_next_tweet(driver)
            tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            for tweet in tweets: 
                alltweets[tweet.text] = 1
            new_size = len(alltweets)
            if oldsize == new_size:
                break


        
        listoftweets = alltweets.keys()
        for tweet in listoftweets:
            try:
                wordcount = tweet.count(ticker)
                if(wordcount):
                    total_occur = total_occur + wordcount
                    occur_for_this_url = occur_for_this_url + wordcount
            except:
                continue
        end_time_for_this_url = time.time()
        elapsed_time_for_this_url = end_time_for_this_url - start_time_for_this_url
        elapsed_time_until_now = end_time_for_this_url - start_time

        print(f' Current URL:  \"{url}\"')
        print(f"\"{ticker}\" was mentioned \"{occur_for_this_url}\" times in the last \"{int(elapsed_time_for_this_url/60)}\" minutes.")
        if(elapsed_time_until_now/60 > interval):
            break

    end_time = time.time()
    elapsed_time = end_time - start_time

    driver.quit()
    return total_occur,elapsed_time


if __name__ == "__main__":
    ticker = "$TSLA"
    interval = 4
    listofurls = ["https://twitter.com/Mr_Derivatives" , 
                  "https://twitter.com/warrior_0719",
                  "https://twitter.com/ChartingProdigy",
                  "https://twitter.com/allstarcharts",
                  "https://twitter.com/yuriymatso",
                  "https://twitter.com/TriggerTrades",
                  "https://twitter.com/AdamMancini4 ",
                  "https://twitter.com/CordovaTrades",
                  "https://twitter.com/Barchart",
                  "https://twitter.com/RoyLMattox"]
    totalocc , timeelapced = app(listofurls, ticker, interval)
    print("-----------------------------------------------------------------------------------------------------------")
    print(f"\"{ticker}\" was mentioned \"{totalocc}\" times in the last \"{int(timeelapced/60)}\" minutes.")
