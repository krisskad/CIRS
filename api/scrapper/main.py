import multiprocessing
from .amazon import AmazonScrape
from .linkedin import LinkedInScrape
from .google import GoogleScrape
# Define functions for scraping Google, Amazon, and LinkedIn


def scrape_google(company_name):
    try:
        google = GoogleScrape()
        google_data = google.scrape(search_term=company_name)
        return google_data
    except Exception as e:
        print(f"Error While Scraping Google: {e}")
        return ""


def scrape_amazon(company_name, uuid):
    try:
        amazon = AmazonScrape(uuid=uuid)
        filepath = amazon.scrape(search_term=company_name)
        return filepath
    except Exception as e:
        print(f"Error While Scraping Amazon: {e}")
        return []


def scrape_linkedin(search_term):
    try:
        linkedin = LinkedInScrape()
        linkedin_data = linkedin.scrape(search_term=search_term)
        return linkedin_data
    except Exception as e:
        print(f"Error While Scraping LinkedIn: {e}")
        return ""


def main(search_term, uuid):
    # Create a multiprocessing pool
    pool = multiprocessing.Pool(processes=3)

    # Define the arguments for each scraping task
    google_args = (search_term,)
    amazon_args = (search_term, uuid)
    linkedin_args = (search_term, )

    # Run the scraping tasks concurrently
    google_result = pool.apply_async(scrape_google, google_args)
    amazon_result = pool.apply_async(scrape_amazon, amazon_args)
    linkedin_result = pool.apply_async(scrape_linkedin, linkedin_args)

    # Get the results from the scraping tasks
    google_data = google_result.get()
    amazon_file = amazon_result.get()
    linkedin_data = linkedin_result.get()

    # Close the multiprocessing pool
    pool.close()
    pool.join()

    return {
        "linkedin": linkedin_data,
        "company_detail":google_data,
        "amazon": amazon_file
    }

