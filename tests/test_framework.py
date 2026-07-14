import unittest
from src.config import Config
from src.tools import TOOL_REGISTRY

class TestBrowserFramework(unittest.TestCase):
    def test_config_defaults(self):
        """Verifies configuration variables load default fallbacks properly[cite: 1]."""
        self.assertIsNotNone(Config.BROWSER_TYPE)
        self.assertTrue(isinstance(Config.HEADLESS, bool))

    def test_tool_registry_initialization(self):
        """Ensures all standard tools are loaded into the registry mapping[cite: 1]."""
        self.assertIn("navigate_to_url", TOOL_REGISTRY)
        self.assertIn("type_text", TOOL_REGISTRY)
        self.assertIn("scroll_page", TOOL_REGISTRY)
        self.assertIn("take_screenshot", TOOL_REGISTRY)

if __name__ == '__main__':
    unittest.main()
