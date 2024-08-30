import math
import os
import re
import time
from datetime import datetime
from urllib.parse import urlparse

import openpyxl
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException


from extract_date_period import calculate_time_interval
from money_verification import contains_money


class SeleniumBrowser:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.driver.maximize_window()

    def find_element_by_xpath(self, xpath:str):
        return self.driver.find_element(By.XPATH, xpath)
    
    def wait_for_xpath_element(self, xpath:str, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    
    def click_element(self, element):
        ActionChains(self.driver).move_to_element(element).click().perform()

    def select_value(self,element, value):
        select = Select(element)
        select.select_by_value(value)

    def navigate(self):
        url = "https://www.aljazeera.com/"   
        self.driver.get(url)
        time.sleep(2)
        try:
            accept_cookies_button = self.wait_for_xpath_element('//button[@id="onetrust-accept-btn-handler"]')
            self.click_element(accept_cookies_button)
        except Exception as e:
            print(f'Error on accept cookies button: {e}')
    
    def save_news_img(self, img_url):
        if not os.path.exists('img'):
            os.makedirs('img')
            
        try:
            img_name = os.path.basename(urlparse(img_url).path)
            img_path = os.path.join('img', img_name)
            
            img_response = requests.get(img_url, stream=True)
            if img_response.status_code == 200:
                with open(img_path, 'wb') as file:
                    for chunk in img_response.iter_content(1024):
                        file.write(chunk)
                return img_name, img_path
            else:
                print(f'Failed to download image: {img_url}')
                return None, None
        except Exception as e:
            print(f'Error saving image: {e}')
        return None, None
    def get_total_results(self):
        try:
            results_text = self.find_element_by_xpath('//*[@id="main-content-area"]/div[2]/div[1]/span[1]').text
            
            total_results = int(re.search(r'\d+', results_text).group())
            return total_results
        except Exception as e:
            print(f'Error getting total results: {e}')
            return 0
    
    def close_ads(self):
        try:
            # Verificar e fechar anúncios, se presentes
            close_ad_buttons = self.driver.find_elements(By.XPATH, '//button[@aria-label="Close Ad"]')
            for button in close_ad_buttons:
                if button.is_displayed():
                    self.click_element(button)
                    time.sleep(1)  # Aguardar um pouco para garantir que o anúncio foi fechado
        except Exception as e:
            print(f'Error closing ads: {e}')

    def load_all_articles(self):
        total_results = self.get_total_results()
        if total_results == 0:
            print("Unable to determine the total number of results.")
            return
        
        # Calcular o número de cliques necessários
        clicks_needed = math.ceil(total_results / 10)
        articles_loaded = 0
        
        for _ in range(clicks_needed):
            self.close_ads()
                
            # Clicar no botão "Show more"
            show_more_button = self.find_element_by_xpath('//button[@class="show-more-button grid-full-width"]')
            if show_more_button.is_displayed():
                self.click_element(show_more_button)
                articles_loaded += 10  # Incrementa o número de artigos carregados
                time.sleep(2)  # Aguardar a carga de mais artigos
            else:
                print('Show more button not found or not clickable.')
 
                
    def extract_news_data(self, months):
        start_date, end_date = calculate_time_interval(months)
        start_date = datetime.strptime(start_date, '%d %b %Y')
        end_date = datetime.strptime(end_date, '%d %b %Y')

        #self.load_all_articles() 

        articles_data = []
        self.close_ads()

        articles = self.driver.find_elements(By.XPATH, '//article')
        
        for article in articles:
            try:
                try:
                    date_text = article.find_element(By.XPATH, './/div[@class="gc__date__date"]//span[@aria-hidden="true"]').text
                    if date_text.startswith('Last update '):
                        date_text = date_text.replace('Last update ', '')
                        pub_date = datetime.strptime(date_text, '%d %b %Y')  
                    else:
                        pub_date = datetime.strptime(date_text, '%d %b %Y')
                except:
                    continue

                # date_text = article.find_element(By.XPATH, './/div[@class="gc__date__date"]//span[@aria-hidden="true"]').text
                # pub_date = datetime.strptime(date_text.replace('Last update ', ''), '%d %b %Y')

                if start_date <= pub_date <= end_date:
                    title = article.find_element(By.XPATH, './/h3[@class="gc__title"]/a/span').text
                    description = article.find_element(By.XPATH, './/div[@class="gc__body-wrap"]//div[@class="gc__excerpt"]/p').text
                    contains_money_info = contains_money(title) or contains_money(description)
                    
                    # img_url = None
                    # try:
                    #     img_element = article.find_element(By.XPATH, './/div[@class="gc__image-wrap"]//img')
                    #     img_url = img_element.get_attribute('src')
                    # except Exception as e:
                    #     print(f'No image found for article: {e}')

                    # img_name, img_path = self.save_news_img(img_url) if img_url else (None, None)

                    article_data = {
                        'title': title,
                        'description': description,
                        'publication_date': pub_date.strftime('%d %b %Y'),
                        'contains_money': contains_money_info,
                    }

                        # 'image_name': img_name,
                        # 'image_path': img_path
                    
                    articles_data.append(article_data)
            
            except Exception as e:
                print(f'Error extracting data from article: {e}')
        
        return articles_data

    def search(self, search_params):
        try:
            query = '+'.join(search_params)
            search_button = self.find_element_by_xpath('//div[@class="site-header__search-trigger"]/button')
            #search_button.click()
            self.click_element(search_button)

            search_input =self.wait_for_xpath_element('//input[@class="search-bar__input"]')
            search_input.send_keys(query)
        
            search_submit = self.find_element_by_xpath('//button[@type="submit"][@aria-label="Search Al Jazeera"]')
            #search_submit.click()
            self.click_element(search_submit)

            select_date = self.wait_for_xpath_element('//select[@id="search-sort-option"]')
            self.select_value(select_date,"date")
   
            time.sleep(2)
        except Exception as e:
            print(f'Error on search: {e}')


    def close_browser(self):
        self.driver.quit()



query = ['israel', 'economy']
month = 3
def main(query, month):
    drive = SeleniumBrowser()
    drive.navigate()
    drive.search(query)
    news_data = drive.extract_news_data(month)
    df = pd.DataFrame(news_data)
    df.to_excel('news_data.xlsx', index=False)

main(query, month)
  
