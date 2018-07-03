from selenium import webdriver
import setting
import time


def get_browser():
    if setting.DEFAULT_BROWSER == 'Chrome':
        browser = webdriver.Chrome()
        options = webdriver.ChromeOptions();
        options.add_argument('headless');
    elif setting.DEFAULT_BROWSER == 'Firefox':
        browser = webdriver.Firefox()
    else:
        browser = webdriver.Chrome()
    return browser


def extract_img_src(browser, crypko_id):
    img = browser.find_elements_by_class_name('progressive-image-main')
    while len(img) == 0 or img[0].get_property('src') == '':
        img = browser.find_elements_by_class_name('progressive-image-main')
        if len(img) == 0 or img[0].get_property('src') == '':
            # browser = get_browser()
            browser.get(setting.CRYPKO_CARD_PAGE.format(crypko_id))
            time.sleep(0.1)
    return img[0].get_property('src')


def extract_attributes(browser, crypko_id):
    attr_tags = browser.find_elements_by_class_name('attr-tag')
    attr_results = []
    for attr_tag in attr_tags:
        if attr_tag.text != '+ Show sub-attributes':
            attr_results.append(attr_tag.text)
        else:
            attr_tag.click()

    return attr_results


def extract_sub_attributes(browser):
    sub_attrs = browser.find_elements_by_class_name('sub-attr')
    sub_attr_results = []
    for sub_attr in sub_attrs:
        sub_attr_results.append(sub_attr.text)
    return sub_attr_results
