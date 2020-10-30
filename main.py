from telethon.sync import TelegramClient
from configparser import ConfigParser
from memberScraper import Scraper
from threading import Lock
import asyncio
import time
from random import randrange

loop = asyncio.get_event_loop()
config = ConfigParser()
config.read('conf.ini')


async def invite(k, v, lock):
    PHONE = config[k]['PHONE_NUMBER_IN_INTERNATIONAL_FORMAT']
    API_ID = config[k]['API_ID']
    API_HASH = config[k]["API_HASH"]
    target_group_name = config['CONF']['TARGET_GROUP_NAME']
    cl = TelegramClient(PHONE, API_ID, API_HASH)
    await cl.connect()
    if not await cl.is_user_authorized():
        await cl.send_code_request(PHONE)
        await cl.sign_in(PHONE, input(f'Enter login/verificatoin code for {PHONE} : '))
    scraper = Scraper(cl, lock, id=API_ID)
    await scraper.scrape(target_group_name)


lock = Lock()
for k, v in config.items():
    if k == 'DEFAULT' or k == 'CONF':
        continue
    loop.create_task(invite(k, v, lock))
    time.sleep(3)


async def keepRunning():
    while True:
        await asyncio.sleep(10000)

loop.run_forever()
