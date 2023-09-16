from playwright.sync_api import sync_playwright


def extract_full_body_html(from_url, wait_for=None):
    # wait for the selected container to load, then extract the HTML <body> from the URL

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(from_url)

        # robust way to make sure that the content we need is loaded before we extract the HTML
        page.wait_for_load_state("networkidle")  # networkidle waits if 0.5s of no network connections/communications
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")  # run js that scrolls to the bottom
        page.wait_for_load_state("domcontentloaded")  # complete when the browser fires the event domcontentloaded

        if wait_for:
            page.wait_for_selector(wait_for)

        # page.screenshot(path="steam3.png", full_page=True) # gives you a screenshot and shows what's rendered

        html = page.inner_html("body")

        return html
