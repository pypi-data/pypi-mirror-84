from selenium import webdriver
import os

from selenium.webdriver.firefox.options import Options as firefox_options
from selenium.webdriver.chrome.options import Options as chrome_options

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def write_to_element_js(driver, element_xpath, input_string):
    """ Function to bypass the send_keys method in selenium when it doesn't work properly.
    Uses JS to do it.
    Found this code by Philipp Doerner in this link: https://stackoverflow.com/questions/18013821/pythons-selenium-send-keys-with-chrome-driver-drops-characters/62135696#62135696
    """
    
    js_command = f'document.evaluate(\'{element_xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = \'{input_string}\';'
    driver.execute_script(js_command)

def write_to_element(driver, element_xpath, input_string, use_js = True):
    """Giving the choice to use the js or the native selenium methods.
    """
    if(use_js):
        write_to_element_js(driver, element_xpath, input_string)
    else:
        driver.find_element_by_xpath(element_xpath).send_keys(input_string)

def choose_webdriver(browser):
    """Choosing availabe webdriver in the webdriver_manager module.

    Args:
        browser (str): browser's name. One of ['chrome', 'chromium', 'firefox', 'ie'].
    """
    if browser == 'chrome':
        options = chrome_options()
        # silent mode
        options.add_argument('--headless')
        # no printing log in the terminal
        options.add_argument("--log-level=3")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    elif browser == 'firefox':
        options = firefox_options()
        # silent mode
        options.headless = True
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), service_log_path=os.devnull, options=options)
    else:
        raise Exception('Your browser is not supported.')

    return(driver) 