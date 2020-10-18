from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon import errors
from telethon.tl.types import InputPeerEmpty
import csv
import os
import random
import time
import sys
from datetime import datetime

# Test

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep


class Scraper:
    def __init__(self, client):
        self.client = client
        f = open('message.txt', 'r')
        self.message = f.read()

    async def scrape(self, target_group_name, **kwargs):
        chats = []
        result = await self.client(GetDialogsRequest(
            offset_date=0,
            offset_id=10,
            offset_peer=InputPeerEmpty(),
            limit=100,
            hash=0
        ))
        chats.extend(result.chats)
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
        print(f'Got list of {len(all_participants)} members ...')
        print('Starting to invite the members in a minute....')
        time.sleep(60)
        for p in all_participants:
            try:
                await self.client.send_message(p, self.message)
            except errors.rpcerrorlist.PeerFloodError:
                print('Got a flood error!\nWaiting for a few seconds...')
                time.sleep(random.randrange(300, 500))
                continue
            print(f'Invite Count: {all_participants.index(p)}')
            time.sleep(random.randrange(15, 30))
