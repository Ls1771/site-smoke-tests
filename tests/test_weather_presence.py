import os, re
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

WEATHER_URL = os.getenv("WEATHER_URL", "https://www.weather.gov/")
TITLE_KEYWORD = os.getenv("TITLE_KEYWORD", "Weather")

@pytest.fixture(scope="session")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    drv = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()

def test_weather_page_presence(driver):
    driver.get(WEATHER_URL)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.TAG_NAME, "body"))
    )
    title = (driver.title or "").strip()
    assert title, "Page title is empty"
    if TITLE_KEYWORD:
        assert re.search(TITLE_KEYWORD, title, re.I), f"Title '{title}' missing '{TITLE_KEYWORD}'"
