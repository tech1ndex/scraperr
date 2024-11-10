from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service




from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def initialize_client() -> None:
    """Initialize a connection to JustWatch API."""
    service = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service)

    try:
        url = "https://www.justwatch.com/ca/provider/netflix/movies"
        driver.get(url)

        # Wait until the movies are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )

        print("Connected Successfully")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        time.sleep(5)
        # Adjust the selector based on inspection
        movies = soup.find_all('a', {'class': 'title'})  # Check if 'title' is still valid


        for movie in movies:
            print(movie.text.strip())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

initialize_client()

time.sleep(3)
