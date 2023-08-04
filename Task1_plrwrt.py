from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://en.wikipedia.org/wiki/Programming_languages_used_in_most_popular_websites")
    browser.close()