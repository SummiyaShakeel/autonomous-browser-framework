import os
import logging
from playwright.sync_api import sync_playwright
from src.config import Config

# Set up clean logging for production errors
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class BrowserEngine:
    def __init__(self):
        self.config = Config()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self, profile_name="default_user"):
        """Initializes Playwright, configures the selected engine,
        and sets up a persistent profile layer for memory management."""
        try:
            self.playwright = sync_playwright().start()

            # Module 5: Create a local directory to persist user profiles, sessions, and cookies
            user_data_dir = os.path.join(os.getcwd(), "browser_profiles", profile_name)
            os.makedirs(user_data_dir, exist_ok=True)

            launch_args = {
                "headless": self.config.HEADLESS,
                "args": [f"--window-size={self.config.WIDTH},{self.config.HEIGHT}"]
            }

            # Module 1 & 3: Multi-browser support via centralized configuration mapping
            # Module 5: launch_persistent_context automatically acts as the Session and Memory Layer
            if self.config.BROWSER_TYPE == "chromium":
                self.context = self.playwright.chromium.launch_persistent_context(user_data_dir, **launch_args)
            elif self.config.BROWSER_TYPE == "firefox":
                self.context = self.playwright.firefox.launch_persistent_context(user_data_dir, **launch_args)
            elif self.config.BROWSER_TYPE == "webkit":
                self.context = self.playwright.webkit.launch_persistent_context(user_data_dir, **launch_args)
            else:
                raise ValueError(f"Unsupported browser type configuration: {self.config.BROWSER_TYPE}")

            # Module 1 & 2: Set global timeout and get the primary page (tab)
            self.context.set_default_timeout(self.config.DEFAULT_TIMEOUT)
            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = self.context.new_page()

            logging.info(f"BrowserEngine initialized successfully utilizing {self.config.BROWSER_TYPE}.")
            return self.page

        except Exception as e:
            logging.error(f"Critical Failure: Failed to initialize Browser Engine. Details: {e}")
            self.close()
            raise

    
    # MODULE 2 & 4: NAVIGATION & INTERACTION LAYER

    def navigate(self, url=None):
        """Navigates to a specific URL with error protection."""
        target_url = url if url else self.config.DEFAULT_URL
        try:
            logging.info(f"Navigating to target URL: {target_url}")
            self.page.goto(target_url, wait_until="load")
        except Exception as e:
            logging.error(f"Navigation failed for URL {target_url}: {e}")

    def create_tab(self):
        """Opens a completely new browser tab (Page)."""
        return self.context.new_page()

    def switch_tab(self, index):
        """Switches execution context to a target tab index."""
        if 0 <= index < len(self.context.pages):
            self.page = self.context.pages[index]
            self.page.bring_to_front()
            return self.page
        logging.warning(f"Tab index {index} out of range bounds.")

    def take_screenshot(self, filepath="screenshot.png", full_page=False):
        """Captures standard or full-page views."""
        self.page.screenshot(path=filepath, full_page=full_page)
        logging.info(f"Screenshot successfully saved to: {filepath}")

    
    # MODULE 3: ADVANCED DOM OPTIMIZATION LAYER
    
    def get_element(self, selector, frame_selector=None):
        """Locates elements reliably across standard page layers or nested iFrames."""
        # Module 3: Locator Strategy optimization & strict handling for iFrames
        base = self.page.frame_locator(frame_selector) if frame_selector else self.page
        return base.locator(selector)

    def extract_data(self, selector):
        """Extracts text, references, and visibility states safely from elements."""
        element = self.get_element(selector).first
        if element.is_visible():
            return {
                "text": element.inner_text(),
                "html": element.inner_html(),
                "href": element.get_attribute("href")
            }
        return None

    
    # MODULE 1 & 5: SHUTDOWN & CLEANUP
   
    def close(self):
        """Gracefully tears down all active pipelines and releases session bindings."""
        logging.info("Closing active browser engine nodes and contexts...")
        try:
            if self.context:
                self.context.close()
            if self.playwright:
                self.playwright.stop()
            logging.info("Teardown operations finalized cleanly.")
        except Exception as e:
            logging.error(f"Error encountered during environment shutdown: {e}")
