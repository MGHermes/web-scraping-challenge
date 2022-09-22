# Web Scraping Dependancies
import requests
from bs4 import BeautifulSoup

# Web Browsing Dependancies
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# Pandas Dependancy
import pandas as pd

# Date-Time Dependancy
import datetime as dt

# Flask Library and Flask-Pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo

# Create instance of Flask app
app = Flask(__name__)

# Create a scrape_all function
def scrape_all():
    # Create a searchable browser (via Splinter)
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Get information from the scrape_news function
    news_title, news_paragraph = scrape_news(browser)

    # Create a super-dictionary (MarsData) of information from the data scrape
    marsData = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": scrape_image(browser),
        "html_table": scrape_facts(browser),
        "list_of_dictionaries": scrape_hemispheres(browser),
        "last_updated": dt.datetime.now()
    }

    # End the browser session
    browser.quit()

    # Return the super-dictionary
    return marsData

# Create a scrape from the news page
def scrape_news(browser):
    # Save and visit the NASA Mars News url
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    # Set the sleep timer
    time.sleep(1)

    # Save the html on the page
    html = browser.html

    # Create a BS Object using this html
    soup = BeautifulSoup(html, "html.parser")

    # Create a list of headlines in the article
    # Located in div class = "content_title"
    headlines = soup.find_all('div', class_='content_title')

    # Store the latest headline: headlines[0]
    news_title = headlines[0].text

    # Create a list of news paragraphs in the article
    # Located in div class = "article_teaser_body"
    paragraphs = soup.find_all('div', class_='article_teaser_body')

    # Store the latest paragraph: paragraphs[0]
    news_p = paragraphs[0].text

    return news_title, news_p

# Create a scrape from the image page
def scrape_image(browser):
    # Save and visit the space image url
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    # Set the sleep timer
    time.sleep(1)

    # Save the html on the page
    html = browser.html

    # Create a BS Object using this html
    soup = BeautifulSoup(html, "html.parser")

    # Save the image info
    # Locate the featured image info in a -> class='showimg fancybox-thumbs'
    imageInfo = soup.find('a', class_='showimg fancybox-thumbs')

    # Identify the url using the href tag
    extension_url = imageInfo['href']

    # Save the complete url using a formatted string
    featured_image_url = f"https://spaceimages-mars.com/{extension_url}"

    return featured_image_url

# Create a scrape from the facts page
def scrape_facts(browser):
    # Save and visit the galaxy facts url
    galaxy_facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(galaxy_facts_url)

    # Set the sleep timer
    time.sleep(1)

    # Save the html on the page
    html = browser.html

    # Create a BS Object using this html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the tables from the webpage using Pandas
    tables = pd.read_html(galaxy_facts_url)

    # Identify the Mars Table: tables[0]
    mars_table = tables[0]

    # Set the first row as the header
    mars_table.columns = mars_table.iloc[0]

    # Drop the first row of the table
    mars_table = mars_table.drop(0)

    # Rename the first column in the table
    mars_table.rename(columns = {'Mars - Earth Comparison':'Description'}, inplace = True)

    # Reset the index to be the description
    mars_table.set_index('Description',inplace=True)
    #mars_table = mars_table.reset_index(drop=True)

    # Convert Pandas DF to Html Table and save it as 'table.html'
    html_table = mars_table.to_html()

    # Remove the extra new line markers
    #html_table = html_table.replace('\n', '')

    return html_table

# Create a scrape from the hemispheres page
def scrape_hemispheres(browser):

    # Save and visit the hemispheres url
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)

    # Set the sleep timer
    time.sleep(1)

    # Save the html on the page
    html = browser.html

    # Create a BS Object using this html
    soup = BeautifulSoup(html, "html.parser")

    # Create a list of dictionaries - one for each hemisphere
    listOfDictionaries = []

    # Create a list of the 4 hemispheres
    hemispheres = []

    # Start by filtering for div class="description"
    # This produces a list that needs further filtering
    hemisphereInfo = soup.find_all('div', class_='description')

    # Next, filtering the list by level 3 headings
    for hemisphere in hemisphereInfo:
        hemisphereName = hemisphere.find('h3').text
        
        # Append the hemisphere name to the list of hemispheres
        hemispheres.append(hemisphereName)

    # Create a loop that goes through each of the hemispheres in the hemisphere list
    for hemisphere in hemispheres:
        #Click on the link for each hemisphere
        browser.links.find_by_partial_text(hemisphere).click()
        
        # Create an empty dictionary
        dictionary = {}
        
        # Set the sleep timer
        time.sleep(1)

        # Save the html on the page
        html = browser.html

        # Create a BS Object using this html
        soup = BeautifulSoup(html, "html.parser")
        
        # Find the link that is titled 'Sample'
        # The Sample link contains the jpg url
        sample = browser.links.find_by_text('Sample')
    
        # Find the href associated with the 'Sample' link
        img_url = sample['href']

        # Remove the word, 'Enhanced,' from the end of the title
        title = hemisphere.replace(" Enhanced","")

        # Add to the dictionary
        dictionary['title']=title
        dictionary['img_url']=img_url
        
        #Add to the list of dictionaries
        listOfDictionaries.append(dictionary)
        
        #Click to go back once the information is collected
        browser.links.find_by_partial_text('Back').click()

    return listOfDictionaries