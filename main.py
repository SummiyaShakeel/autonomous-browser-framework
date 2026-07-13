import time
import logging
from src.browser_engine import BrowserEngine
from src.human_behavior import HumanBehaviorEngine


def run_automation_pipeline():
    logging.info("--- Starting Autonomous Framework Execution Pipeline ---")

    engine = BrowserEngine()

    try:
        # 1. Initialize Core Engine with Session Profile Memory (Module 1 & 5)
        page = engine.start(profile_name="internship_agent_01")
        human = HumanBehaviorEngine(page)

        # 2. Navigate to Google (Module 2 & 4)
        engine.navigate("https://google.com")
        human.trigger_random_idle()

        # 3. Type search query humanly (Module 3 & 4)
        search_input_selector = "[name='q']"
        logging.info("Executing realistic search typing routine...")
        human.human_type(search_input_selector, "Python Playwright advanced human automation framework")

        # 4. Submit Search and wait for layout container (Module 2 & 3)
        logging.info("Submitting search query...")
        page.keyboard.press("Enter")

        logging.info("Waiting for search results page to render...")
        page.wait_for_selector("#search", timeout=90000)
        time.sleep(2)

        # 5. Scroll and "read" the Google results page (Module 4)
        logging.info("Scrolling search results page...")
        human.human_scroll_and_read(scrolls=2)

        # 6. MODULE 4 (TASK 5) & MODULE 3: FIND AND CLICK A REAL WEBSITE LINK
        # This selector targets the main organic result header links on Google safely
        result_link_selector = "#search a h3"

        if page.locator(result_link_selector).count() > 0:
            logging.info("Target link detected. Simulating human hover and click to visit website...")
            # Hover naturally, pause, and click the link (Module 2 & 4)
            human.human_hover_and_click(result_link_selector)

            # Wait for the external website to load completely
            page.wait_for_load_state("load")
            logging.info(f"Successfully navigated to external site: {page.url}")
            time.sleep(3)

            # Scroll and read inside the new website (Module 4 Navigation/Reading flow)
            logging.info("Reading and scrolling through the chosen target website...")
            human.human_scroll_and_read(scrolls=2)

            # Module 2 & 4: Simulate a natural browser history back action
            logging.info("Simulating human clicking 'Back' to return to search results...")
            page.go_back()
            page.wait_for_load_state("load")
            time.sleep(2)
        else:
            logging.warning("No search result headers found to click.")

        # 7. Capture Final Proof of Work Output (Module 2)
        engine.take_screenshot(filepath="outputs/final_search_result.png", full_page=False)
        logging.info("Pipeline executed seamlessly with zero unexpected failures!")

        logging.info("Holding browser open for final inspection...")
        time.sleep(5)

    except Exception as general_error:
        logging.critical(f"Pipeline crashed safely during runtime operation: {general_error}")

    finally:
        # 8. Safe System Resource Teardown Protocol (Module 1)
        engine.close()
        logging.info("--- Automation Pipeline Session Terminated Gracefully ---")


if __name__ == "__main__":
    import os

    os.makedirs("outputs", exist_ok=True)
    run_automation_pipeline()