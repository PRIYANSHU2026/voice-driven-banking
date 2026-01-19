from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from voicebank.actions.base import ActionExecutor
from voicebank.models import CommandResult
import os


class SeleniumExecutor(ActionExecutor):
    def __init__(self):
        self._driver = None

    def _get_driver(self):
        if self._driver is None:
            opts = Options()
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
        return self._driver

    def execute(self, action: str, params: Dict[str, Any]) -> CommandResult:
        if not os.getenv("ALLOW_SELENIUM", "0") == "1":
            return CommandResult(success=False, message="Selenium disabled. Set ALLOW_SELENIUM=1 to enable.")

        try:
            if action == "open_demo_site":
                driver = self._get_driver()
                driver.get("https://example.com")
                title = driver.title
                return CommandResult(success=True, message=f"Opened site with title: {title}")
            return CommandResult(success=False, message=f"Unknown action: {action}")
        except Exception as e:
            return CommandResult(success=False, message=str(e))

    def __del__(self):
        try:
            if self._driver is not None:
                self._driver.quit()
        except Exception:
            pass
