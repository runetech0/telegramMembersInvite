from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon import errors
from telethon.tl.types import InputPeerEmpty
import csv
import os
from asyncio import sleep
import random
import time
import sys
from datetime import datetime
import shelve

# Test

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


class Scraper:
    def __init__(self, client, lock, id=None):
        self.client = client
        self.id = id
        self.lock = lock
        f = open('message.txt', 'r')
        self.message = f.read()
        f.close()

    async def scrape(self, target_group_name, **kwargs):
        if not os.path.exists('./SessionFiles'):
            os.mkdir('./SessionFiles')
        chats = []
        result = await self.client.get_dialogs()
        chats.extend(result)
        target_group = None
        for chat in chats:
            if chat.title == target_group_name:
                target_group = chat
                break
        if target_group is None:
            print('Could Not find the target group to scrape members ...')
            sys.exit(1)
        all_participants = []
        print('Getting a list of all the members ...')
        all_participants = await self.client.get_participants(target_group, aggressive=True)
        await sleep(10)
        for p in all_participants:
            while True:
                if self.lock.locked():
                    await sleep(0.2)
                    continue
                self.lock.acquire()
                break
            shelf = shelve.open('./SessionFiles/data')
            try:
                lastIndex = shelf[target_group_name]
            except KeyError:
                shelf[target_group_name] = 0
                lastIndex = 0
            shelf.sync()
            if all_participants.index(p) <= lastIndex:
                shelf.sync()
                shelf.close()
                self.lock.release()
                await sleep(1)
                continue
            try:
                await self.client.send_message(p, self.message)
                # shelf = shelve.open('./SessionFiles/data')
                shelf[target_group_name] = all_participants.index(p)
                try:
                    count = shelf[f'{target_group_name}_count']
                except KeyError:
                    shelf[f'{target_group_name}_count'] = 1
                count = shelf[f'{target_group_name}_count']
                shelf[f'{target_group_name}_count'] = count + 1
                print(f'Invite Count: {count}')
                shelf.sync()
                shelf.close()
                self.lock.release()
                await sleep(random.randrange(100, 120))
                continue
            except errors.rpcerrorlist.PeerFloodError:
                print("Telegram requests rate limit detected !")
                shelf.sync()
                shelf.close()
                self.lock.release()
                await sleep(random.randrange(300, 500))
                continue
            except errors.rpcerrorlist.FloodWaitError as e:
                print(
                    f'Telegram wants us to wait for {e.seconds} before sending the next request ...')
                shelf.sync()
                shelf.close()
                self.lock.release()
                await sleep(e.seconds + 5)
                continue
