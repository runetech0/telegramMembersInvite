from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerChat
import telethon.errors as TelegramErrors
import csv
from inviter import Inviter
import os
from memberScraper import Scraper
from configparser import ConfigParser
import asyncio


conf = ConfigParser()
conf.read('conf.ini')

api_id = conf['CONF']['API_ID']
api_hash = conf['CONF']['API_HASH']
phone = conf['CONF']['PHONE_NUMBER_IN_INTERNATIONAL_FORMAT']
target_group_name = conf['CONF']['TARGET_GROUP_NAME']

async def main():
    if not os.path.exists('./SessionFiles'):
        os.mkdir('./SessionFiles')
        print(f'Using account : {phone}')
        print(f'Target group name : {target_group_name}')
    client = TelegramClient(f'./SessionFiles/{phone}', api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input(f'Enter login/verificatoin code for {phone} : '))
    scraper = Scraper(client)
    await scraper.scrape(target_group_name)
    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())