import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)



def scrape_info():
    browser = init_browser()

    mars_info = {}
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    html = browser.html
    soup = bs(html,"html.parser")
    news_headline = soup.find("div", class_ = "content_title").text
    mars_info["News"] = news_headline
    news_teaser = soup.find("div", class_ = "article_teaser_body").text
    mars_info["Teaser"] = news_teaser
    


    base_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(base_url)  
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(10)

    browser.click_link_by_partial_text("more info")
    time.sleep(10)

    image_html = browser.html
    image_soup = bs(image_html, "html.parser")
    image_url = image_soup.find('img', class_="main_image").get("src")
    complete_url = "https://www.jpl.nasa.gov" + image_url
    


    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)   
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'html.parser')
    tweets = twitter_soup.find('div', attrs={'class': 'tweet', "data-name":'Mars Weather'})
    mars_weather = tweets.find('p', 'tweet-text').get_text()
   

  
    mars_facts = "http://space-facts.com/mars/"
    browser.visit(mars_facts)
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns=['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    mars_facts = mars_df.to_html()
    mars_facts = mars_facts.replace("\n", "")

    hemi_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, "html.parser")
    results = hemi_soup.find_all("h3")
    hemi_list_of_dicts=[]
    for result in results:
        title = result.text  
        browser.click_link_by_partial_text(title)
        hemi_individ_html = browser.html
        hemi_individ_soup = bs(hemi_individ_html, "html.parser")
        url = hemi_individ_soup.find('a', target="_blank").get("href")
        hemi_list_of_dicts.append({'title': title, 'URL': url})
        browser.click_link_by_partial_text('Back')
   
    latest_mars_data = {}
    latest_mars_data['mars_news'] = mars_info
    latest_mars_data['mars_image'] = complete_url
    latest_mars_data['mars_weather'] = mars_weather
    latest_mars_data['mars_facts'] = mars_facts
    latest_mars_data['mars_hemispheres']= hemi_list_of_dicts

    browser.quit()
    
    return latest_mars_data