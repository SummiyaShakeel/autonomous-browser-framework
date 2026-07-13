import time
import random
import logging


class HumanBehaviorEngine:
    def __init__(self, page):
        """Initializes the behavior framework linked to the current active page."""
        self.page = page

    # ==========================================
    # TASK 1: HUMAN TYPING SIMULATION
    # ==========================================
    def human_type(self, selector, text, error_rate=0.07):
        """Simulates realistic human typing patterns with varying delay speeds,
        intentional random typos, backspaces, and natural self-corrections."""
        element = self.page.locator(selector)
        element.click()  # Focus the field first

        for char in text:
            # Task 1 & 6: Simulate a human typo mistake based on error probability distribution
            if random.random() < error_rate and char.isalpha():
                wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                element.type(wrong_char)
                time.sleep(random.uniform(0.15, 0.4))  # Human reaction time delay

                # Perform backspace correction
                self.page.keyboard.press("Backspace")
                time.sleep(random.uniform(0.1, 0.25))

            # Type the correct character with randomized delays (Simulates varying WPM strings)
            element.type(char)
            time.sleep(random.uniform(0.05, 0.18))

        logging.info(f"Human-like text typed successfully into selector: {selector}")

    # ==========================================
    # TASK 2: HUMAN MOUSE MOVEMENT & HOVER
    # ==========================================
    def human_hover_and_click(self, selector):
        """Moves to an element naturally, hovers briefly, and clicks with dynamic timing."""
        element = self.page.locator(selector).first

        # Human actions hover over targeted links or buttons before interacting
        element.hover()
        time.sleep(random.uniform(0.3, 0.7))  # Micro-pause before deciding to click

        element.click()
        logging.info(f"Human-like hover and click action completed on: {selector}")

    # ==========================================
    # TASK 3 & 4: HUMAN SCROLLING & READING PAUSES
    # ==========================================
    def human_scroll_and_read(self, scrolls=3):
        """Simulates human user reading patterns, scrolling down dynamic amounts,
        pausing briefly to consume content, and occasionally back-scrolling slightly."""
        for i in range(scrolls):
            # Calculate a random scroll distance sequence
            scroll_distance = random.randint(300, 700)
            self.page.evaluate(f"window.scrollBy(0, {scroll_distance});")
            logging.info(f"Scrolled down by {scroll_distance}px")

            # Task 4: Simulate a brief reading/idle attention-span pause
            time.sleep(random.uniform(1.5, 4.0))

            # Task 3: 20% chance the user returns or scrolls back slightly to review text
            if random.random() < 0.2:
                back_scroll = random.randint(100, 250)
                self.page.evaluate(f"window.scrollBy(0, -{back_scroll});")
                time.sleep(random.uniform(0.8, 1.5))

    # ==========================================
    # TASK 5: NATURAL IDLE INACTIVITY
    # ==========================================
    def trigger_random_idle(self):
        """Generates unexpected long idle micro-delays mimicking short interruptions."""
        if random.random() < 0.15:  # 15% chance of checking phone/distraction pause
            idle_time = random.uniform(3.0, 7.0)
            logging.info(f"Simulating natural human idle distraction for {idle_time:.2f}s...")
            time.sleep(idle_time)
