from selenium import webdriver
import util
import setting
import json
import os

if __name__ == '__main__':
    browser = webdriver.Chrome()
    if not os.path.exists(setting.SAVE_DIR):
        os.makedirs(setting.SAVE_DIR)

    for crypko_id in range(1, setting.CRYPKO_MAX_ID + 1):
        print('====== {} ======='.format(crypko_id))

        if not os.path.exists(setting.SAVE_FILENAME.format(crypko_id)):
            browser.get(setting.CRYPKO_CARD_PAGE.format(crypko_id))
            img_src = util.extract_img_src(browser, crypko_id)
            tags = util.extract_attributes(browser, crypko_id)

            print('img: {}'.format(img_src))
            print('tags: {}'.format(tags))

            with open(setting.SAVE_FILENAME.format(crypko_id), 'w') as f:
                json.dump({
                    'img': img_src,
                    'tags': tags
                }, f)
