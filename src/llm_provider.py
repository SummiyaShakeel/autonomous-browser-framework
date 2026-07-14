import logging

logger = logging.getLogger("LLMProvider")


class BaseLLMProvider:
    """Abstract Base Class for LLM API Abstraction (Adapter Pattern)."""

    def generate_response(self, system_prompt, user_prompt, tools=None):
        raise NotImplementedError("Each provider must implement generate_response")


class MockLocalProvider(BaseLLMProvider):
    """Fallback local execution model simulating cognitive thinking and planning."""

    def generate_response(self, system_prompt, user_prompt, tools=None):
        logger.info("[LLM Provider] Analyzing context and generating step-by-step plan via cognitive logic...")

        # We enrich the AI's plan to make it perform a complete, realistic workflow
        if "google.com" in user_prompt:
            return {
                "thought": "I need to open Google, search for the target topic, submit the query, navigate into a result, scroll to read, and capture proof.",
                "plan": [
                    # Step 1: Open the search engine
                    {"tool": "navigate_to_url", "args": {"url": "https://google.com"}},

                    # Step 2: Type search text with human simulation
                    {"tool": "type_text", "args": {"selector": "[name='q']", "text": "AI Multi-Agent Swarms"}},

                    # Step 3: Scroll the Google search results page
                    {"tool": "scroll_page", "args": {"scrolls": 2}},

                    # Step 4: Click the first search result link to enter the website
                    {"tool": "click_element", "args": {"selector": "#search a h3"}},

                    # Step 5: Scroll down to "read" the chosen website
                    {"tool": "scroll_page", "args": {"scrolls": 2}},

                    # Step 6: Save the final screenshot
                    {"tool": "take_screenshot", "args": {"filepath": "outputs/ai_swarm_result.png"}}
                ]
            }

        return {
            "thought": "Direct objective unclear, reverting to default exploration route.",
            "plan": [{"tool": "navigate_to_url", "args": {"url": "https://google.com"}}]
        }