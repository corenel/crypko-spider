from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import setting
import time
import sys


def get_browser():
    """
    Get browser by setting

    :return: browser instance
    :rtype: webdriver.Chrome
    """
    if setting.DEFAULT_BROWSER == 'Chrome':
        browser = webdriver.Chrome()
        options = webdriver.ChromeOptions();
        options.add_argument('headless');
    elif setting.DEFAULT_BROWSER == 'Firefox':
        browser = webdriver.Firefox()
    else:
        browser = webdriver.Chrome()
    return browser


def extract_img_src(browser):
    """
    Extract source link of avatar image from web page

    :param browser: opened browser
    :type browser: webdriver.Chrome
    :return: source link of avatar image
    :rtype: str
    """
    img = browser.find_elements_by_class_name('progressive-image-main')
    cnt_failed = 0
    flag_success = False
    while not flag_success:
        img = browser.find_elements_by_class_name('progressive-image-main')
        if cnt_failed >= 10:
            browser.refresh()
            cnt_failed = 0
        if len(img) == 0 or \
                (len(img) > 0 and img[0].get_property('src') == '') or \
                (len(img) > 0 and '_lg.jpg' not in img[0].get_property('src')):
            time.sleep(1)
            try:
                curr_url = browser.current_url
                browser.get(curr_url)
                # browser.refresh()
            except TimeoutException:
                continue
            cnt_failed += 1
        else:
            flag_success = True
    return img[0].get_property('src')


def extract_attributes(browser):
    """
    Extract attribute tags of avatar image from web page

    :param browser: opened browser
    :type browser: webdriver.Chrome
    :return: attribute tags of avatar image
    :rtype: list
    """
    attr_tags = browser.find_elements_by_class_name('attr-tag')
    attr_results = []
    for attr_tag in attr_tags:
        if attr_tag.text != '+ Show sub-attributes':
            attr_results.append(attr_tag.text)
        else:
            attr_tag.click()

    return attr_results


def extract_sub_attributes(browser):
    """
    Extract sub attribute tags of avatar image from web page

    :param browser: opened browser
    :type browser: webdriver.Chrome
    :return: sub attribute tags of avatar image
    :rtype: list
    """
    sub_attrs = browser.find_elements_by_class_name('sub-attr')
    sub_attr_results = []
    for sub_attr in sub_attrs:
        sub_attr_results.append(sub_attr.text)
    return sub_attr_results
