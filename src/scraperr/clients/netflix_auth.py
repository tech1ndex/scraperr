from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from scraperr.logger import logger
import time
from typing import Any

class NetflixClient:
    """Client that allows interaction with Netflix via Selenium."""

    def __init__(self):
        self.driver = None
        self.wait = None

    def initialize_driver(self) -> None:
        """Initialize Chrome WebDriver and WebDriverWait."""
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)

    def terminate_driver(self) -> None:
        """Safely close the WebDriver connection."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None

    def wait_and_find_element(self, by: By, value: str, clickable: bool = False) -> Any:
        """Wait for and return an element."""
        condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        return self.wait.until(condition((by, value)))

    def safe_click(self, element) -> bool:
        self.driver.execute_script("arguments[0].click();", element)
        return True


    def login(self, url: str, username: str, password: str, profile: str) -> bool:
        """Login to Netflix and select profile."""
        try:
            self.initialize_driver()
            self.driver.get(url)

            # Login form
            username_field = self.wait_and_find_element(
                By.CSS_SELECTOR, "input[data-uia='login-field']"
            )
            username_field.send_keys(username)
            logger.info("Entered Username")

            password_field = self.wait_and_find_element(
                By.CSS_SELECTOR, "input[data-uia='password-field']"
            )
            password_field.send_keys(password)
            logger.info("Entered Password")

            sign_in_button = self.wait_and_find_element(
                By.XPATH, "//button[contains(text(), 'Sign In')]",
                clickable=True,
            )
            sign_in_button.click()
            logger.info("Clicked Sign In")

            # Profile selection
            self.wait_and_find_element(By.CLASS_NAME, "profile-gate-label")
            profile_button = self.wait_and_find_element(
                By.XPATH, f"//span[contains(text(), '{profile}')]",
                clickable=True,
            )
            logger.info("Found Profile Button")

            # Wait for loading states
            try:
                loading_spinner = self.wait_and_find_element(By.CLASS_NAME, "loading-spinner")
                self.wait.until(EC.staleness_of(loading_spinner))
            except:
                logger.error("Could not load states")

            # Click profile with retry logic
            if self.safe_click(profile_button):
                logger.info("Loaded Profile")
                time.sleep(20)  # Consider replacing with explicit wait
                return True

            return False

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
        finally:
            self.terminate_driver()

    def get_movies(self, url: str) -> list:
        """Fetch movies from Netflix."""
        try:
            self.initialize_driver()
            self.driver.get(url)
            # Add your movie scraping logic here
            return []
        except Exception as e:
            logger.error(f"Error fetching movies: {e}")
            return []
        finally:
            self.terminate_driver()
