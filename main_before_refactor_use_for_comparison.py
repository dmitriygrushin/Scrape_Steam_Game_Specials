from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

""" Learning Outcomes: """
"""
Learning Outcome #1: JavaScript Scraping with Playwright
    https://store.streampowered.com/specials
    * title
    * link to thumbnail
    * category tags
    * rating
    * # of reviews
    * original price
    * discounted price
    * discount %
    
Learning Outcome #2: Code Organization & Project Structure & Separation of Concerns
    [render JS with Playwright] 
    -- html --> 
        [extract elements from HTML based on .json config] - config.json = generic utility i.e. parse_raw_attributes 
            -- raw attributes -->
                [apply functional transforms, if any]
                    -- save --> 
                        [yyyy_mm_dd_extract.csv] """

URL = "https://store.steampowered.com/specials"

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        # robust way to make sure that the content we need is loaded before we extract the HTML
        page.wait_for_load_state("networkidle")  # networkidle waits if 0.5s of no network connections/communications
        page.evaluate("() => window.scroll(0, document.body.scrollHeight)")  # run js that scrolls to the bottom
        page.wait_for_load_state("domcontentloaded")  # complete when the browser fires the event domcontentloaded
        page.wait_for_selector('div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]')  # wait for the selector

        # page.screenshot(path="steam3.png", full_page=True) # gives you a screenshot and shows what's rendered
        html = page.inner_html("body")

        tree = HTMLParser(html)

        # [*=]: contains, [=]: absolute match
        # game container - divs is a list of games
        divs = tree.css('div[class*="salepreviewwidgets_StoreSaleWidgetContainer"]')

        print(len(divs))

        for d in divs:
            title = d.css_first('div[class*="StoreSaleWidgetTitle"]').text()
            thumbnail = d.css_first('img[class*="CapsuleImage"]').attributes.get("src")
            tags = [a.text() for a in d.css('div[class*="StoreSaleWidgetTags"] > a')[:5]]
            release_date = d.css_first(
                'div[class*="WidgetReleaseDateAndPlatformCtn"] > div[class*="StoreSaleWidgetRelease"]').text()
            review_score = d.css_first('div[class*="ReviewScoreValue"] > div').text()
            reviewed_by = d.css_first('div[class*="ReviewScoreCount"]').text()
            sale_price = d.css_first('div[class*="StoreSalePriceBox"]').text()
            original_price = "Free" if not d.css_first('div[class*="StoreOriginalPrice"]') else d.css_first('div[class*="StoreOriginalPrice"]').text()

            """
            review_score = "N/A" if not d.css_first('div[class*="ReviewScoreValue"] > div') else d.css_first(
                'div[class*="ReviewScoreValue"] > div').text()
            reviewed_by = "N/A" if not d.css_first('div[class*="ReviewScoreCount"]') else d.css_first(
                'div[class*="ReviewScoreCount"]').text()
            sale_price = d.css_first('div[class*="StoreSalePriceBox"]').text()
            original_price = "Free" if not d.css_first('div[class*="StoreOriginalPrice"]') else d.css_first(
                'div[class*="StoreOriginalPrice"]').text()
            """

            attrs = {
                "title": title,
                "original_price": original_price,
                "sale_price": sale_price,
                "review_score": review_score,
                "release_date": release_date,
                "tags": tags,
                "thumbnail": thumbnail,
                "reviewed_by": reviewed_by
            }

            print(attrs)
