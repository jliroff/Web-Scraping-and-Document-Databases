
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)

def scrape():
	browser = init_browser()
	mars_data = {}

    #JPL Mars Space Images - Featured Image
	jpl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl)

	html = browser.html
	soup = BeautifulSoup(html, "html.parser")

	picture_link = soup.find('a',class_='button fancybox')
	featured_image = picture_link['data-fancybox-href']

	featured_image_url = 'https://www.jpl.nasa.gov' + featured_image
	mars_data['Feature Image URL'] = featured_image_url


	#Mars Weather
	twitter = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(twitter)

	html = browser.html
	soup2 = BeautifulSoup(html, "html.parser")

	mars_weather = soup2.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text.strip()
	mars_data['Mars Weather'] = mars_weather


    #Mars Hemispheres
	mars_data['Hemisphere image urls'] = [
	{"title":"Cerberus Hemisphere","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
	{"title":"Schiaparelli Hemisphere","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
	{"title":"Syrtis Major Hemisphere","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
	{"title":"Valles Marineris Hemisphere","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"}
	]

	#Mars Facts
	marsfacts_url = 'https://space-facts.com/mars/'
	marsfacts = pd.read_html(marsfacts_url)

	marsfacts_pd = marsfacts[0]
	marsfacts_pd = marsfacts_pd.rename(columns={0:'Description',1:'Value'})
	marsfacts_pd = marsfacts_pd.set_index('Description')

	mars_facts_html=marsfacts_pd.to_html(justify='left')

	mars_data['Mars Facts'] = mars_facts_html

	#NASA Mars News
	mars_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

	response = requests.get(mars_news)
	soup3 = BeautifulSoup(response.text, 'html.parser')

	news_title = soup3.find_all('div', class_='content_title')[0].find('a').text.strip()
	news_p = soup3.find_all("div", class_='image_and_description_container')[0].text.strip()

	mars_data['News Title'] = news_title
	mars_data['News Description'] = news_p

	return mars_data
