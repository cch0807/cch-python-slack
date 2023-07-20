import time
from playwright.sync_api import sync_playwright

# play = sync_playwright().start()
# play.stop()

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False, channel="msedge")
    page = browser.new_page()

    page.goto("https://www.naver.com")
    time.sleep(3)
