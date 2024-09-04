
import time
from datetime import datetime

import requests
from RPA.Browser.Selenium import Selenium

from .extract_date_period import calculate_time_interval
from .manage_files import create_image_path
from .money_verification import contains_money
from .search_phrase_count import count_search_phrase


class SeleniumBrowser:
    def __init__(self):
        self.driver = Selenium()
        self.driver.open_available_browser(
            url="https://www.aljazeera.com/",  
            options={"arguments": ["--inprivate"]}
        )  
        self.image_count = 0 

    def find_element_by_xpath(self, xpath: str):
        return xpath
    def find_element(self, xpath: str):
        return self.driver.find_element(xpath)
    
    
    def wait_for_xpath_element(self, xpath: str, timeout=10):
        self.driver.wait_until_element_is_visible(xpath, timeout)
        return xpath 

    def click_element(self, element):
        self.driver.click_element(element)


    def select_value(self, element, value):
        self.driver.select_from_list_by_value(element, value)
    def navigate(self):
        url = "https://www.aljazeera.com/"   
        self.driver.go_to(url)
        time.sleep(2)
        try:
            accept_cookies_button = self.wait_for_xpath_element('//button[@id="onetrust-accept-btn-handler"]')
            self.click_element(accept_cookies_button)
        except Exception as e:
            print(f'Error on accept cookies button: {e}')
    def close_ads(self):
        try:
            close_ad_buttons = self.driver.find_elements('//button[@aria-label="Close Ad"]')

            for button in close_ad_buttons:
                self.driver.click_element_if_visible(button)
                time.sleep(1)  
        except Exception as e:
            print(f'Error closing ads: {e}')
    def load_all_articles(self):
        while True:
            try:
                self.close_ads()
                show_more_button = self.wait_for_xpath_element('//button[@class="show-more-button grid-full-width"]', timeout=10)
                self.click_element(show_more_button)
                time.sleep(2)  
            except Exception as e:
                print(f'No more articles to load or error: {e}')
                break 
    def salve_image(self, image_url):
        self.image_count += 1
        image_name = f'Imagem_{self.image_count:02}.jpg'
        image_path = create_image_path(image_name)
        try:
            response = requests.get(image_url)
            response.raise_for_status()  
            
            with open(image_path, 'wb') as f:
                f.write(response.content)
            #print(f'Image saved successfully: {image_path}')
        
        except Exception as e:
            print(f'Error saving image {image_url}: {e}')
        
        return image_name
    def extract_news_date(self, article):
        try:
            date_text = article.find_element('xpath','.//div[@class="gc__date__date"]//span[@aria-hidden="true"]').text

            if date_text.startswith('Last update '):
                date_text = date_text.replace('Last update ', '')
            pub_date = datetime.strptime(date_text, '%d %b %Y')
            return pub_date 
        except Exception as e:
            print(f'News does not have a publication date: {e}')
            return None
    def extract_news_data(self,search_phrase, months):
        start_date_str, end_date_str = calculate_time_interval(months)
        start_date = datetime.strptime(start_date_str, '%d %b %Y')
        end_date = datetime.strptime(end_date_str, '%d %b %Y')

        self.load_all_articles() 

        articles_data = []
        articles = self.driver.find_elements('//article')
        
        for article in articles:
            try:
                pub_date = self.extract_news_date(article)
                if pub_date is not None and start_date <= pub_date <= end_date:
                    title = article.find_element('xpath','.//h3[@class="gc__title"]/a/span').text
                    news_url = article.find_element('xpath','.//a[@class="u-clickable-card__link"]').get_attribute('href')
                    description = article.find_element('xpath','.//div[@class="gc__body-wrap"]//div[@class="gc__excerpt"]/p').text                 
                    contains_money_info = contains_money(title) or contains_money(description)
                    search_term_frequency = count_search_phrase(search_phrase, title, description)

                    try:
                        image_element = article.find_element('xpath','.//div[@class="gc__image-wrap"]//img[@class="article-card__image gc__image"]')
                        image_url = image_element.get_attribute('src')
                        image_name = self.salve_image(image_url)
                    except:
                        image_name = None

                    article_data = {
                        'title': title,
                        'description': description,
                        'publication_date': pub_date.strftime('%d %b %Y'),
                        'search_phrase_count': search_term_frequency,
                        'contains_money': contains_money_info,
                        'image_name': image_name,
                        'image_url': image_url,
                        'news_url':news_url
                    }
                    
                    articles_data.append(article_data)
            
            except Exception as e:
                print(f'Error extracting data from article: {e}')
        
        return articles_data

    def search(self, search_params):
        try:
            query = '+'.join(search_params)
            search_button = self.find_element_by_xpath('//div[@class="site-header__search-trigger"]/button')
            self.click_element(search_button)

            search_input = self.wait_for_xpath_element('//input[@class="search-bar__input"]')
            self.driver.input_text(search_input, query)
        
            search_submit = self.find_element_by_xpath('//button[@type="submit"][@aria-label="Search Al Jazeera"]')
            self.click_element(search_submit)

            select_date = self.wait_for_xpath_element('//select[@id="search-sort-option"]')
            self.select_value(select_date, "date")
   
            time.sleep(2)
        except Exception as e:
            print(f'Error on search: {e}')
    def close_browser(self):
        self.driver.close_browser()