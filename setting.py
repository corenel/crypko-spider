import os

CRYPKO_CARD_PAGE = 'https://crypko.ai/#/card/{}'
CRYPKO_MAX_ID = 574290

SAVE_DIR = 'data'
SAVE_JSONNAME = os.path.join(SAVE_DIR, '{:09d}.json')
SAVE_FILENAME = os.path.join(SAVE_DIR, '{:09d}.jpg')

# DEFAULT_BROWSER = 'Firefox'
DEFAULT_BROWSER = 'Chrome'

NUM_PROCESS = 8
