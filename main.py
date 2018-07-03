from selenium import webdriver

import argparse
import requests
import json
import time
import os

import util
import setting

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Spider for Crypko')
    parser.add_argument('--from', '-f', type=int, default=1, help='Start id')
    parser.add_argument('--to', '-t', type=int, default=setting.CRYPKO_MAX_ID, help='Stop id')
    args = vars(parser.parse_args())

    if not os.path.exists(setting.SAVE_DIR):
        os.makedirs(setting.SAVE_DIR)

    browser = util.get_browser()

    for crypko_id in range(args['from'], args['to'] + 1):
        print('====== {} ======='.format(crypko_id))
        start = time.time()
        if not os.path.exists(setting.SAVE_FILENAME.format(crypko_id)):
            browser.get(setting.CRYPKO_CARD_PAGE.format(crypko_id))

            img_src = util.extract_img_src(browser, crypko_id)
            tags = util.extract_attributes(browser, crypko_id)

            print('img: {}'.format(img_src))
            print('tags: {}'.format(tags))

            if img_src:
                with open(setting.SAVE_JSONNAME.format(crypko_id), 'w') as f:
                    json.dump({
                        'img': img_src,
                        'tags': tags
                    }, f)

                r = requests.get(img_src)
                with open(setting.SAVE_FILENAME.format(crypko_id), 'wb') as f:
                    f.write(r.content)
        print('elapsed: {} s'.format(time.time() - start))
