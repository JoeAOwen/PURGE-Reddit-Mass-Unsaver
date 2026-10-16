import argparse
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BROWSERS = {"chrome": webdriver.Chrome, "firefox": webdriver.Firefox, "safari": webdriver.Safari}

# div.content > div#siteTable > div#thing_tX_xxxxx
ITEMS = "#siteTable > div[id^='thing_']"
SAVE_LINK = ".//li[contains(@class,'save-button')]/a | .//a[contains(@class,'save')]"


def wait_for_listing(driver):
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "siteTable")))
    except TimeoutException:
        pass


def unsave_page(driver, include, exclude, delay, dry_run):
    """Unsave matching items on the current page. Returns number handled."""
    wait_for_listing(driver)
    things = driver.find_elements(By.CSS_SELECTOR, ITEMS)
    print(f"Page {driver.current_url}: found {len(things)} item(s)")

    if not things:  # diagnostics: shows e.g. a block page or wrong URL
        body = driver.find_element(By.TAG_NAME, "body").text[:300].replace("\n", " ")
        print(f"  Page title: {driver.title!r}\n  Page text starts: {body!r}")
        return 0

    count = 0
    for thing in things:
        sub = (thing.get_attribute("data-subreddit") or "").lower()
        if (include and sub not in include) or sub in exclude:
            continue
        link = None
        for candidate in thing.find_elements(By.XPATH, SAVE_LINK):
            if (candidate.get_attribute("textContent") or "").strip().lower() == "unsave":
                link = candidate
                break
        if link is None:
            continue
        print(f"  {'Would unsave' if dry_run else 'Unsaving'} [r/{sub}] {thing.get_attribute('id')}")
        count += 1
        if not dry_run:
            driver.execute_script("arguments[0].click();", link)
            random_delay = random.uniform(delay * 0.5, delay * 1.5)
            time.sleep(random_delay)

    if things and count == 0:
        print("  Items found but no 'unsave' link matched (all filtered out, or markup differs).")
    return count

def main():
    arg_parser = argparse.ArgumentParser(description="Unsaver for Reddit")
    arg_parser.add_argument("--browser", choices=BROWSERS, default="firefox")
    arg_parser.add_argument("--include", nargs="*", default=[], help="Only unsave from these subreddits")
    arg_parser.add_argument("--exclude", nargs="*", default=[], help="Do not unsave from these subreddits")
    arg_parser.add_argument("--dry-run", action="store_true", help="Actually unsave (default is dry run)")
    arg_parser.add_argument("--delay", type=float, default=0.9, help="Time in seconds between unsaves (average)")
    args = arg_parser.parse_args()

    include = {s.lower().removeprefix("r/") for s in args.include}
    exclude = {s.lower().removeprefix("r/") for s in args.exclude}

    driver = BROWSERS[args.browser]()
    try:
        driver.get("https://old.reddit.com/login")
        input("Log in to Reddit in the browser window, then press Enter here... ")

        driver.get("https://old.reddit.com/")
        username = driver.find_element(By.CSS_SELECTOR, "span.user a").text
        url = f"https://old.reddit.com/user/{username}/saved"
        driver.get(url)
        print(f"Logged in as {username}\n")

        total = 0
        while True:
            handled = unsave_page(driver, include, exclude, args.delay, args.dry_run)
            total += handled
            if handled and not args.dry_run:
                driver.get(driver.current_url)  # reload: remaining items shift up
                continue
            try:  # nothing (left) to do here, move to next page
                driver.find_element(By.CSS_SELECTOR, "span.next-button a").click()
            except NoSuchElementException:
                break

        print(f"\n{'Would unsave' if args.dry_run else 'Unsaved'} {total} item(s).")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
