from multiprocessing import Process

import argparse
import requests
import json
import time
import sys
import os

import util
import setting


def image_crawl(begin_id, end_id):
    """
    Single process for crawling images

    :param begin_id: beginning id of image to crawl
    :type begin_id: int
    :param end_id: ending id of image to crawl
    :type end_id: int
    """
    browser = util.get_browser()
    for crypko_id in range(begin_id, end_id + 1):
        if not os.path.exists(setting.SAVE_FILENAME.format(crypko_id)):
            start = time.time()
            browser.get(setting.CRYPKO_CARD_PAGE.format(crypko_id))
            time.sleep(1)

            img_src = util.extract_img_src(browser)
            tags = util.extract_attributes(browser)

            if img_src:
                with open(setting.SAVE_JSONNAME.format(crypko_id), 'w') as f:
                    json.dump({
                        'img': img_src,
                        'tags': tags
                    }, f)

                try:
                    r = requests.get(img_src)
                    with open(setting.SAVE_FILENAME.format(crypko_id), 'wb') as f:
                        f.write(r.content)
                except requests.exceptions.SSLError:
                    print('SSL error when downloading image file, skip this one')

            print('====== {} ======='.format(crypko_id))
            print('img: {}'.format(img_src))
            print('tags: {}'.format(tags))
            print('elapsed: {} s'.format(time.time() - start))


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Spider for Crypko')
    parser.add_argument('--from', '-f', type=int, default=1, help='Start id')
    parser.add_argument('--to', '-t', type=int, default=setting.CRYPKO_MAX_ID, help='Stop id')
    parser.add_argument('--mp', action='store_true', help='Use multi-processing')
    args = vars(parser.parse_args())

    # check save directory
    if not os.path.exists(setting.SAVE_DIR):
        os.makedirs(setting.SAVE_DIR)

    if not args['mp']:
        image_crawl(args['from'], args['to'])
    else:
        # intialize process
        cnt = 0
        step = (args['to'] - args['from']) // setting.NUM_PROCESS
        process_list = []
        for i in range(setting.NUM_PROCESS):
            p = Process(target=image_crawl, args=(args['from'] + cnt * step,
                                                  args['from'] + (cnt + 1) * step))
            process_list.append(p)
            cnt += 1

        # start processes
        try:
            for p in process_list:
                p.start()
        except KeyboardInterrupt:
            for p in process_list:
                p.join()
            sys.exit(0)
        except:
            for cnt, p in enumerate(process_list):
                if not p.is_alive() or p.exitcode is not None:
                    # re-create and start
                    p = Process(target=image_crawl, args=(args['from'] + cnt * step,
                                                          args['from'] + (cnt + 1) * step))
                    process_list.insert(cnt, p)
                    p.start()
