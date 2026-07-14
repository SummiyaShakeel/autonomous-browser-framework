import logging

class BaseTool:
    """Abstract base class that all browser tools must inherit from."""
    name = "BaseTool"
    description = "Defines the base interface for agent browser execution units."

    def execute(self, engine, **kwargs):
        raise NotImplementedError("Each tool must implement its own execute logic.")


class NavigateTool(BaseTool):
    name = "navigate_to_url"
    description = "Navigates the browser to a specific URL."

    def execute(self, engine, url, **kwargs):
        logging.info(f"[Tool: Navigate] Opening URL: {url}")
        engine.navigate(url)
        return f"Successfully navigated to {url}"


class ClickTool(BaseTool):
    name = "click_element"
    description = "Hovers naturally and clicks an element matching the CSS or XPath selector."

    def execute(self, engine, selector, human_behavior=None, **kwargs):
        logging.info(f"[Tool: Click] Targeting element: {selector}")
        if human_behavior:
            human_behavior.human_hover_and_click(selector)
        else:
            engine.get_element(selector).first.click()
        return f"Successfully clicked selector '{selector}'"


class TypeTool(BaseTool):
    name = "type_text"
    description = "Enters text into an input field and optionally submits it."

    def execute(self, engine, selector, text, press_enter=True, human_behavior=None, **kwargs):
        logging.info(f"[Tool: Type] Typing text into selector: {selector}")
        if human_behavior:
            human_behavior.human_type(selector, text)
        else:
            engine.get_element(selector).first.fill(text)

        # Automatically press enter to submit search queries
        if press_enter:
            logging.info("[Tool: Type] Pressing Enter key...")
            engine.page.keyboard.press("Enter")

        return f"Successfully typed text and submitted '{selector}'"

class ScrollTool(BaseTool):
    name = "scroll_page"
    description = "Scrolls the webpage down or up dynamically to read content."

    def execute(self, engine, scrolls=1, human_behavior=None, **kwargs):
        logging.info(f"[Tool: Scroll] Scrolling layout {scrolls} times")
        if human_behavior:
            human_behavior.human_scroll_and_read(scrolls=scrolls)
        else:
            engine.page.evaluate("window.scrollBy(0, 500);")
        return f"Successfully completed {scrolls} scroll operations"


class ScreenshotTool(BaseTool):
    name = "take_screenshot"
    description = "Captures a screenshot of the current viewport."

    def execute(self, engine, filepath="outputs/agent_capture.png", **kwargs):
        logging.info(f"[Tool: Screenshot] Capturing view to {filepath}")
        engine.take_screenshot(filepath=filepath)
        return f"Screenshot saved successfully to {filepath}"


# Global Registry of tools for easy routing
TOOL_REGISTRY = {
    NavigateTool.name: NavigateTool(),
    ClickTool.name: ClickTool(),
    TypeTool.name: TypeTool(),
    ScrollTool.name: ScrollTool(),
    ScreenshotTool.name: ScreenshotTool()
}