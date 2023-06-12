import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import math
import re
from collections import Counter

WORD = re.compile(r"\w+")
import re
from .VirtualDisplayCodeAndTranslate import SmartDisplayWithTranslate


class LinkedInScrape:
    def __init__(self, email=None, password=None):
        if not email:
            self.email = "krishna.kadam@ongil.ai"
        if not password:
            self.password = "mynameis@krishna"

        self.smt_dsp = SmartDisplayWithTranslate()
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape(self, search_term=None):
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)
        # Use login credentials to login
        email = self.driver.find_element(By.XPATH, '//*[@id="username"]')
        email.send_keys(self.email)
        password = self.driver.find_element(By.XPATH, '//*[@id="password"]')
        password.send_keys(self.password)
        time.sleep(3)
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        # search keyword
        self.driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={search_term}")

        # get list of companies urls
        elems = self.driver.find_elements(By.XPATH,
                                     '//*[@class="entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light"]//a')
        company_list = []
        for elem in elems:
            company_url = elem.get_attribute("href")
            company_list.append(company_url)
        print(company_list)
        # extract company name from url
        final_name = ""
        company_name_score = []
        for url in company_list:
            if isinstance(url, str):
                final_name = self.get_company_name(url)
                if final_name and isinstance(final_name, str):
                    vector1 = self.text_to_vector(final_name)
                    vector2 = self.text_to_vector(search_term)

                    cosine = self.get_cosine(vector1, vector2)
                    company_name_score.append({"company_name":final_name, "score":cosine})
        temp_df = pd.DataFrame(company_name_score)
        print(temp_df)
        if len(temp_df)>0:
            final_name = temp_df[temp_df['score'] == temp_df['score'].max()]['company_name'].tolist()[0]
        print(final_name)
        # use company name to extract company info
        if final_name:
            company_page = f"https://www.linkedin.com/company/{final_name}/"
            self.driver.get(f"https://www.linkedin.com/company/{final_name}/about/")
            overview = self.driver.find_element(By.XPATH, '//*[@class="mb6"]').text
            self.driver.get(company_page)
            company_heading = self.driver.find_element(By.XPATH, '//*[@class="block mt2"]').text
            overview = f"URL: {company_page} \n\n {company_heading} \n\n {overview}"

        else:
            overview = ""

        try:
            self.smt_dsp.stopSmartDisplay()
        except:
            pass

        return overview

    def get_company_name(self, url):
        # Define the regular expression pattern
        pattern = r'https:\/\/www\.linkedin\.com\/company\/(.+)\/'

        # Use re.findall() to extract the company name
        matches = re.findall(pattern, url)

        # Extracted company name will be stored in the first element of the matches list
        if matches:
            company_name = matches[0]
        else:
            company_name = ""

        return company_name

    def get_cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(self, text):
        words = WORD.findall(text)
        return Counter(words)
