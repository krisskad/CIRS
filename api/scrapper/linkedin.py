from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


class LinkedInScrape:
    def __init__(self, email=None, password=None):
        if not email:
            self.email = "krishna.kadam@ongil.ai"
        if not password:
            self.password = "mynameis@krishna"

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

        # extract company name from url
        final_name = ""
        for url in company_list:
            final_name = self.get_company_name(url)
            if final_name:
                break

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
