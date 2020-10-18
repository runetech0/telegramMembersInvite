import csv
import time
from telethon import utils


class Inviter:
    def __init__(self, client):
        self.client = client


    async def invite(self, csv_list):
        users = []
        with open(csv_list, encoding='UTF-8') as f:
            rows = csv.reader(f,delimiter=",",lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['seq_no'] = row[0]
                user['username'] = row[1]
                user['id'] = int(row[2])
                user['access_hash'] = int(row[3])
                user['name'] = row[4]
                users.append(user)
        en = await self.client.get_entity(users[190]['id'])
        await en.send_message('Hello')