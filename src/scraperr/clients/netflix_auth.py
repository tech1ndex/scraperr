from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)
from scraperr.logger import logger
import time
from typing import Any

class NetflixClient:
    def __init__(self):
        self.driver = None
        self.wait = None

    def __enter__(self):
        """Context manager entry"""
        self.initialize_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.terminate_driver()

    def initialize_driver(self) -> None:
        """Initialize Chrome WebDriver and WebDriverWait."""
        if not self.driver:
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
        if not self.driver:
            raise RuntimeError("Driver not initialized")
        condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
        return self.wait.until(condition((by, value)))

    def safe_click(self, element, max_attempts: int = 3) -> bool:
        """Safely click an element with retry logic."""
        if not self.driver:
            raise RuntimeError("Driver not initialized")
            
        for attempt in range(max_attempts):
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    raise
                continue
            except WebDriverException as e:
                logger.error(f"Click attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_attempts - 1:
                    raise
                continue
        return False

    def login(self, url: str, username: str, password: str, profile: str) -> bool:
        """Login to Netflix and select profile."""
        try:
            self.driver.get(url)
            
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
                clickable=True
            )
            sign_in_button.click()
            logger.info("Clicked Sign In")

            self.wait_and_find_element(By.CLASS_NAME, "profile-gate-label")
            profile_button = self.wait_and_find_element(
                By.XPATH, f"//span[contains(text(), '{profile}')]",
                clickable=True
            )
            logger.info("Found Profile Button")

            try:
                loading_spinner = self.wait_and_find_element(By.CLASS_NAME, "loading-spinner")
                self.wait.until(EC.staleness_of(loading_spinner))
            except TimeoutException:
                pass  # Loading spinner might not appear

            if self.safe_click(profile_button):
                logger.info("Loaded Profile")
                # Replace sleep with explicit wait for some element that indicates profile is loaded
                self.wait_and_find_element(By.CLASS_NAME, "browse")  # or another appropriate selector
                return True
            return False

        except (TimeoutException, WebDriverException) as e:
            logger.error(f"Error during login: {e}")
            return False

    def get_movies(self, url: str) -> list:
        """Fetch movies from Netflix."""
        try:
            self.driver.get(url)
            # Add your movie scraping logic here
            return []
        except WebDriverException as e:
            logger.error(f"Error fetching movies: {e}")
            return []