
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
	mars_data['Feature_Image_URL'] = featured_image_url


	#Mars Weather
	twitter = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(twitter)

	html = browser.html
	soup2 = BeautifulSoup(html, "html.parser")

	mars_weather = soup2.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text.strip()
	mars_data['Mars_Weather'] = mars_weather


	#Mars Hemispheres
	hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hem)


	# HTML object
	html = browser.html
    
	# Parse HTML with Beautiful Soup
	soup4 = BeautifulSoup(html, 'html.parser')

    
	mars_dic = {}
	mars_url_links = []

	results = soup4.find_all('h3')

	for result in results:
		item = result.text
    
		browser.click_link_by_partial_text(item)
    
    	# HTML object
		xhtml = browser.html
    
		# Parse HTML with Beautiful Soup
		soup5 = BeautifulSoup(xhtml, 'html.parser')
    
		link = soup5.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
    
		mars_dic["title"] = item
		mars_dic["img_url"] = link
    
		mars_url_links.append(mars_dic)
    
		mars_dic = {}
    
		browser.click_link_by_partial_text('Back')

	mars_data['mars_url_links'] = mars_url_links

	#Mars Facts
	marsfacts_url = 'https://space-facts.com/mars/'
	marsfacts = pd.read_html(marsfacts_url)

	marsfacts_pd = marsfacts[0]
	marsfacts_pd = marsfacts_pd.rename(columns={0:'Description',1:'Value'})
	marsfacts_pd = marsfacts_pd.set_index('Description')

	mars_facts_html=marsfacts_pd.to_html(justify='left')

	mars_data['Mars_Facts'] = mars_facts_html

	#NASA Mars News
	mars_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

	response = requests.get(mars_news)
	soup3 = BeautifulSoup(response.text, 'html.parser')

	news_title = soup3.find_all('div', class_='content_title')[0].find('a').text.strip()
	news_p = soup3.find_all("div", class_='image_and_description_container')[0].text.strip()

	mars_data['News_Title'] = news_title
	mars_data['News_Description'] = news_p

	return mars_data
