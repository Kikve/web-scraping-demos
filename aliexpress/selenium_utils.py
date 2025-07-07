# ====================
# Selenium utils
# ====================

import logging
from typing import Optional
import re
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
import time
from typing import Tuple

# ============================================================

logger = logging.getLogger("myapp")

# ============================================================


def get_driver(
    user_agent,
    window_size: Tuple[int, int] = (1200, 800),
    headless: bool = False,
    chrome_driver_path="./chromedriver",
    timeout=30,
) -> ChromeDriver:
    """
    Create and configure a Chrome WebDriver instance.

    Args:
        user_agent: The User-Agent string to send with each request.
        headless: Whether to run Chrome in headless mode (no GUI). Defaults to False.
        window_size: Initial window size as (width, height). Defaults to (1200, 800).
        page_load_timeout: Maximum seconds to wait for page loads. Defaults to 30.
        chrome_driver_path: Filesystem path to the chromedriver executable.

    Returns:
        A configured instance of selenium.webdriver.chrome.webdriver.WebDriver.

    Raises:
        RuntimeError if the driver binary is missing or fails to start.
    """

    options = Options()
    if headless:
        options.add_argument("headless=new")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"window-size={window_size[0]},{window_size[1]}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = Service(executable_path=chrome_driver_path)

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        raise RuntimeError(
            f"[get_driver] failed to start ChromeDriver at '{chrome_driver_path=}'"
        ) from e

    driver.set_page_load_timeout(30)

    return driver


def driver_info(driver: WebDriver) -> dict:
    # User Agent
    ua = driver.execute_script("return navigator.userAgent")
    _, ip = get_IP(driver)

    # if these are missing can be interpretated as a bot
    platform = driver.execute_script("return navigator.platform")
    vendor = driver.execute_script("return navigator.vendor")
    languages = driver.execute_script("return navigator.languages")
    webdriver = driver.execute_script("return navigator.webdriver")  # should be false

    # real users has variaty of sizes on these variables
    width = driver.execute_script("return screen.width")
    height = driver.execute_script("return screen.height")
    dpr = driver.execute_script("return window.devicePixelRatio")
    tz = driver.execute_script(
        "return Intl.DateTimeFormat().resolvedOptions().timeZone"
    )

    # bots often have empty plugins
    plugins = driver.execute_script(
        "return Array.from(navigator.plugins).map(p=>p.name)"
    )
    mimeTypes = driver.execute_script(
        "return Array.from(navigator.mimeTypes).map(m=>m.type)"
    )

    # bots not persist or send real cookies
    cookies = driver.get_cookies()
    ls = driver.execute_script("return window.localStorage")
    ss = driver.execute_script("return window.sessionStorage")

    keys = [
        "ua",
        "ip",
        "platform",
        "vendor",
        "languages",
        "webdriver",
        "width",
        "height",
        "dpr",
        "tz",
        "plugins",
        "mimeTypes",
        "cookies",
        "ls",
        "ss",
    ]
    ns = locals().copy()
    return {name: ns[name] for name in keys}


def get_IP(driver: WebDriver) -> Tuple[bool, Optional[str]]:
    if navigate_to(driver, "https://www.whatismyip.com/"):
        time.sleep(5)
        ip = driver.find_element(By.ID, "ipv4").text
        return (True, ip)
    else:
        return (False, None)


def scroll_end(
    driver: WebDriver,
    scroll_step: int = 1600,
    pause_time: float = 1.0,
    bottom_threshold: int = 1000,
) -> bool:
    """
    Scrolls the page down in increments until you’ve reached (or are within)
     a certain distance of the bottom of the document.

     Args:
         driver: A Selenium WebDriver instance.
         scroll_step: Number of pixels to scroll in each iteration. Defaults to 1600.
         pause_time: Seconds to wait after each scroll. Defaults to 1.0.
         bottom_threshold: Stop when the remaining distance to the bottom is less
           than this number of pixels. Defaults to 1000.
         max_steps: Maximum number of scroll attempts before giving up. Defaults to 100.

     Returns:
         True if the bottom was reached (within bottom_threshold),
         False if the page are not scrolling.

    """

    height = driver.execute_script("return document.body.scrollHeight")
    position_height = driver.execute_script("return window.scrollY")
    while (height - position_height) > bottom_threshold:
        driver.execute_script(
            f"window.scrollTo({position_height}, {position_height + scroll_step});"
        )

        # Get the new values
        time.sleep(pause_time)
        height = driver.execute_script("return document.body.scrollHeight")
        position_height = driver.execute_script("return window.scrollY")

    logger.info(f"[scroll end] url = {driver.current_url}, end scroll")
    return True


def get_page_soup(driver: WebDriver) -> BeautifulSoup:
    """
    Retrieve the current page’s HTML and parse it into a BeautifulSoup object.

    # Args:
    driver (WebDriver): An already-configured Selenium WebDriver
        that has navigated to the desired URL.

    # Returns:
    BeautifulSoup: The parsed HTML of the current page, using
    the built-in 'html.parser'.
    """
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    return soup


def select_and_hover(driver: WebDriver, selector: str, retry: int = 2) -> bool:
    """
    Find and element in current driver page ans hover it

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        retry (int): Number of times to attempt selection

    Returns:
        bool:
            True if the page was successfully loaded (via driver.get),
            False if all attempts failed and the page was skipped.
    """

    for attempt in range(0, retry):
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            ActionChains(driver).move_to_element(element).perform()
            logger.info(f"[selector_and_hover] => {selector=},{attempt=} hovered")

            return True

        except (TimeoutException, NoSuchElementException):
            logger.error(f"[selector_and_hover] => {selector=},{attempt=} not found")

        except WebDriverException:
            logger.error(f"Navigation Error {attempt=}")

        if attempt < retry:
            input("Press return to continue")
        else:
            logger.error(f"[selector_and_hover] => {selector=},{attempt=} skipping")
            return False


def parse_product_page_to_dict(
    soup_product: BeautifulSoup, popup_class: str
) -> Tuple[bool, dict]:
    """
    Parses a product page popup table into a dictionary of key-value pairs.

    This function locates a popup by its CSS class, finds the first table inside it,
    and extracts each row into key-value entries. It builds a dictionary where the
    first column is used as the key and the second column as the value.

    # Args
    soup_product (BeautifulSoup): A BeautifulSoup object of the current HTML page.
    popup_class (str): The CSS class name of the popup container.

    # Returns
    Tuple[bool,dict]:
        Returns False if the expected popup/table format is missing, otherwise
        prints the collected data and returns True.
    """
    popup = soup_product.find(class_=popup_class)
    table = popup.table if popup else None
    data = {}

    if not table or not popup:
        logger.error(
            f"[parse_product_page_to_dict] format is not right =>{popup=},{table=}"
        )
        return (False, data)

    for tr in table.children:
        x, y = tr.children
        x = x.get_text(strip=True).replace(":", "")
        y = y.get_text(strip=True)

        data[x] = y

    logger.info("[parse_product_page_to_dict] data recolected => {popup_class=}")
    return (True, data)


def card_to_dict(card_component: BeautifulSoup) -> Tuple[bool, dict]:
    """
    Parses a card component into a dictionary with name, price and url.

    Args:
        card_component (BeautifulSoup): A BeautifulSoup tag representing a single product card.

    Returns:
        Tuple[bool, dict]:
            (True, data) if parsing succeeded with extracted info.
            (False, {}) if structure was not as expected.
    """

    link_tag = card_component.find("a")
    name_tag = card_component.find(class_="kr_j0")
    price_tag = card_component.find(class_="kr_kj")

    if not all((link_tag, name_tag, price_tag)):
        logger.error(
            f"[card_to_dict] format is not right => {link_tag=},{name_tag=},{price_tag=}"
        )
        return (False, {})

    url = link_tag.get("href", "").strip()
    product_name, price_text = [e.get_text(strip=True) for e in (name_tag, price_tag)]

    price = extract_number(price_text)

    logger.info(
        f"[card_to_dict] soup parsed to dict product_name={product_name[:20]} ... , {price=}"
    )

    return (
        True,
        {
            "name": product_name,
            "price": price,
            "url": "https:" + url,
        },
    )


def extract_number(string_number: str) -> Tuple[bool, Optional[float]]:
    """
    Extracts the first number (with optional decimal point) from a string.

    Returns (True, value) on success, or (False, 0.0) on no match.
    Commas are stripped before parsing.
    """
    string_number = string_number.strip().replace(",", "")
    match = re.search(r"[\d\.]+", string_number)
    if match:
        number = match.group(0)
        return True, float(number)
    else:
        return False, None


def navigate_to(driver: WebDriver, url: str) -> bool:
    """
    Navigate the Selenium WebDriver to the given URL, returning success status.

       Args:
           driver (WebDriver): An instance of Selenium’s WebDriver.
           url (str): The destination URL to load.

       Returns:
           bool:
               - True if the page was loaded without exception.
               - False if an exception occurred while loading, with the error logged
    """
    try:
        driver.get(url)
    except Exception as e:
        logger.error(f"[navigate_to] page not loaded -> {e}")
        return False
    time.sleep(1)
    current_url = driver.current_url
    if current_url != url:
        logger.error(f"[navigate to] the page returned is not the same {current_url}")
        input("Press Return to continue")
        navigate_to(driver, url)
    logger.info(f"[navigate to] page loaded {url}")
    return True


def get_info_seller(
    driver: WebDriver, url: str, selector_popup: str, selector_product: str
) -> Tuple[bool, dict]:
    """
    1) Load `url` via navigate_to().
    2) Hover element `selector_popup` via select_and_hover().
    3) Parse product details under `selector_product`.

    Returns:
        (True, product_dict) if everything succeeds.
        (False, {}) if load, hover or parse fails.
    """

    if navigate_to(driver, url) and select_and_hover(driver, selector_popup):
        soup_product = get_page_soup(driver)
        status, product_dict = parse_product_page_to_dict(
            soup_product, selector_product
        )
        return (True, product_dict) if status else (False, {})
    else:
        return (False, {})
