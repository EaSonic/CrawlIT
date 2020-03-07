#!/usr/bin/env python

import itchat
import requests
import json
from bs4 import BeautifulSoup
import re

import datetime
import time
from signal import signal, SIGINT

def logout(sigrecv, frame):
    itchat.logout()
    exit(0)

if __name__ == '__main__':
    # Wechat setting
    itchat.auto_login()
    mask_room = itchat.search_chatrooms(name='COVID')
    mask_room_id = mask_room[0]['UserName']
    print(mask_room_id)

    # Run every 5 minutes
    while True:
        signal(SIGINT, logout)

        now = datetime.datetime.now()
        if now.minute % 5 == 0 and now.second == 0:
        # if now.second % 2 == 0:
            face_mask_riteaid = {'url': 'https://www.riteaid.com/shop/rite-aid-health-care-ear-loop-face-mask-20-ct-8021972',
                                 'name': 'RiteAid Face Mask'}
            response = requests.get(face_mask_riteaid['url'])
            sp_fm_ra = BeautifulSoup(response.content, features="lxml")
            
            info = sp_fm_ra.find("script", text=re.compile("var dlObjects")).text.split("\n")

            info = filter(lambda x: x.find('var dlObjects =')>0, info)
            info = list(info)
            mask_info = info[0].lstrip().split('=')

            riteaid_face_mask_info = json.loads(mask_info[1].strip().split(';')[0])[0]
            print("{}: {}".format(face_mask_riteaid["name"], 
                                    riteaid_face_mask_info['ecommerce']['detail']['products'][0]['price']), 
                                    riteaid_face_mask_info['ecommerce']['detail']['products'][0]['dimension4'].upper())
            print(now)

            time.sleep(1)

            if (riteaid_face_mask_info['ecommerce']['detail']['products'][0]['dimension4'].upper() != "OUT OF STOCK") or (now.hour == 8 and now.minute == 0):
                itchat.send("口罩: {},\n价格: {},\n库存: {}\n网址: {}".format(riteaid_face_mask_info['ecommerce']['detail']['products'][0]['name'], 
                                                riteaid_face_mask_info['ecommerce']['detail']['products'][0]['price'],
                                                riteaid_face_mask_info['ecommerce']['detail']['products'][0]['dimension4'].upper(),
                                                face_mask_riteaid['url']), toUserName=mask_room_id)

    logout()