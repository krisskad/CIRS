from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import pandas as pd

import csv
from io import StringIO
from django.core.files.base import ContentFile


class AmazonScrape:
    def __int__(self):
        pass

    def scrape(self, search_term=None, pages=3):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        filename = self.create_file()

        for page_num in range(1, pages):
            search_keyword = search_term.replace(" ", "+")
            url = f'https://www.amazon.com/s?k={search_keyword}&page={str(page_num)}&ref=nb_sb_noss_2'
            driver.get(url)
            time.sleep(3)
            driver.execute_script("window.scrollBy(0,12500)")
            time.sleep(3)
            product_tiles = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
            product_position = 1

            for tile in product_tiles:
                data = dict()
                data['SearchTerm'] = search_term
                data['PageNum'] = page_num
                data['Rank'] = product_position
                product_position += 1
                try:
                    tile.find_element(By.XPATH, './/a[@class="s-label-popover s-sponsored-label-text"]')
                    data['Sponsered'] = True
                except NoSuchElementException:
                    data['Sponsered'] = False
                try:
                    data['ProductURL'] = tile.find_element(By.XPATH,
                                                           './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute(
                        'href').split('?')[0]
                except:
                    data['ProductURL'] = None
                try:
                    data['Title'] = tile.find_element(By.XPATH,
                                                      './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/span').text
                except:
                    data['Title'] = None
                try:
                    data['ASIN'] = tile.get_attribute('data-asin')
                except:
                    data['ASIN'] = None
                try:
                    data['SalesPrice'] = tile.find_element(By.XPATH, './/span[@class="a-price"]/span[2]').text
                except:
                    data['SalesPrice'] = None
                try:
                    data['ListPrice'] = tile.find_element(By.XPATH,
                                                          './/span[@class="a-price a-text-price"]/span[2]').text
                except:
                    data['ListPrice'] = None
                try:
                    data['RatingsCount'] = tile.find_element(By.XPATH,
                                                             './/div[@class="a-row a-size-small"]/span[2]').get_attribute(
                        'aria-label')
                except:
                    data['RatingsCount'] = None
                try:
                    data['AvgRating'] = tile.find_element(By.XPATH,
                                                          './/div[@class="a-row a-size-small"]/span[1]').get_attribute(
                        'aria-label')
                except:
                    data['AvgRating'] = None

                temp_df = pd.DataFrame([data])
                # df = pd.concat([df, temp_df], ignore_index=True)
                temp_df.to_csv(filename, index=False, mode='a', header=False)
        return {
            "filename":filename,
        }

    def create_file(self, filename=None):
        cols_list = ['SearchTerm', 'PageNum', 'Rank', 'Sponsered', 'ProductURL', 'Title', 'ASIN', 'SalesPrice',
                     'ListPrice', 'RatingsCount', 'AvgRating']
        df = pd.DataFrame(columns=cols_list)

        if filename is None:
            filename = f"amazon_{str(datetime.datetime.now())}.csv"

        df.to_csv(filename, index=False)

        return filename