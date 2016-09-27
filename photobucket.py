from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, \
                                       NoSuchElementException, \
                                       WebDriverException
import time


# The starting URL. It can be the URL of any album element.
START_URL = r"http://s536.photobucket.com/user/Bezduszny/media/5SMYYR2YXE/VideoDJ9.mp4.html?sort=3&o=0"

# The number of items in the album to download.
NO_ITEMS = 375


if __name__ == "__main__":
    # Launch the Chrome browser driven by Selenium Webdriver.
    wd = webdriver.Chrome()

    # Go to the start URL and initialize the loop.
    wd.get(START_URL)
    pageno = 0
    retrying = False
    
    # Continue looping until all album elements have been processed.
    while pageno < NO_ITEMS:

        # Increase the page counter if we are not retrying to download
        # from the current page.
        if not retrying:
            pageno += 1
            print("Doing element {0}".format(pageno))
        retrying = False

        try:
            # Find the "Download" button in the page source and click it.
            download = wd.find_element_by_id("download")
            download.click()

            # Find the "Next" button and click it.
            next_arrow = wd.find_element_by_id("next")
            next_arrow.click()

        except (ElementNotVisibleException, WebDriverException) as e:
            # Ads popped up which prevented us from clicking a button.
            # We will try to close them.

            if (type(e) is WebDriverException 
                    and "not clickable" not in e.message):
                # This is not the exception we are looking for, we need to 
                # raise it again since it's unexpected and we
                # can't handle it.
                raise

            print("Ads came up. Waiting 5s...")
            time.sleep(5)

            # Find the first ad close button and click it.
            closead = wd.find_element_by_xpath(
                    "//button[@class='close'][@aria-label='Close']"
                    )
            closead.click()
            print("    Closed ad 1")
            time.sleep(1)

            try:
                # Find the second ad close button and click it.
                closead = wd.find_element_by_id("ac_148699_modal-close")
                closead.click()
                print("    Closed ad 2")
            except NoSuchElementException:
                print("    Ad 2 did not come up")

            # We will be retrying to download from the current page
            # instead of advancing to a new one, so we remember
            # this information.
            retrying = True

