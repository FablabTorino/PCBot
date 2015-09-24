#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

''' This Bot prints breadboards layout on a thermal printer '''

import telegram
import time
import calendar
import datetime
from conversation import *
import string
import json
import urllib

import printer
import privateData

# Telegram Bot Authorization Token
# SuperMario_bot
bot = telegram.Bot(privateData.token)
#AUGChatId=str(-22985187)
#AUGChatId=str(-26538515)
AUGChatId=str(-6549559)

DataUrl="https://raw.githubusercontent.com/FablabTorino/PCBot/master/data/printable.json"
GFXUrl="https://raw.githubusercontent.com/FablabTorino/PCBot/master/gfx/"

# This will be our global variable to keep the latest update_id when requesting
# for updates. It starts with the latest update_id if available.
try:
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
except IndexError:
    LAST_UPDATE_ID = None


   # custom_keyboard = [[ telegram.Emoji.THUMBS_UP_SIGN,   telegram.Emoji.THUMBS_DOWN_SIGN ]]
   # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
   # bot.sendMessage(chat_id=chat_id, text="Stay here, I'll be back.", reply_markup=reply_markup)


import string
import re
import random




def echo():
    global LAST_UPDATE_ID
    # Request updates from last updated_id
    try:
        for update in bot.getUpdates(offset=LAST_UPDATE_ID):
            if LAST_UPDATE_ID < update.update_id:
                # chat_id is required to reply any message
                chat_id = update.message.chat_id
                from_user = update.message.from_user
                if update.message.text!=None:
                    # message = update.message.text.encode('utf-8')
                    message = update.message.text
                    message = message.encode('utf-8')
                    #print message here
                    print(message)
                else: message=None
                print(from_user)
                if (message):
                    #this stuff is not core of the printing breadboard layout stuff... just as reference
                    if '\AUGcalendar' in message:
                        AUGCalendar()
                        LAST_UPDATE_ID = update.update_id
                        return
                    elif '/breadboards_list' in message:
                        breadboards_list(chat_id)
                        LAST_UPDATE_ID = update.update_id
                        return
                    elif '/breadboard_' in message:
                        message=message.replace("/breadboard_","")
                        #print message
                        print_breadboard(message, chat_id)
                        LAST_UPDATE_ID = update.update_id
                        return
                    elif '/help' in message: #please fix this
                        print 'attaccati al tram'
                        bot.sendMessage(chat_id=chat_id, text="Please help me! I'm stuck here! It's a me, Mario!")
                        LAST_UPDATE_ID = update.update_id
                        return
                    else :
                        print 'default'
                        bot.sendMessage(chat_id=chat_id, text="What is "+message+"?")
                        LAST_UPDATE_ID = update.update_id
                        return

                if (message):
                    if '#print' in message:
                        bot.sendMessage(chat_id=chat_id, text=message)
                        #bot.sendMessage(chat_id=chat_id, text=therapist.respond(message))
                        LAST_UPDATE_ID = update.update_id
                LAST_UPDATE_ID = update.update_id
    except:
        pass


def AUGCalendar():
    # Compute the dates for each week that overlaps the month
    now = datetime.datetime.now()
    print str(now)
    year=now.year
    month=now.month
    c = calendar.monthcalendar(year, month)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]
    fourth_week = c[3]
    fifth_week = c[4]

    # If there is a WEDNESDAY in the first week, the second WEDNESDAY
    # is in the second week.  Otherwise the second Thursday must
    # be in the third week.
    if first_week[calendar.WEDNESDAY]:
        Ameeting_date = second_week[calendar.WEDNESDAY]
        Bmeeting_date = fourth_week[calendar.WEDNESDAY]
    else:
        Ameeting_date = third_week[calendar.WEDNESDAY]
        Bmeeting_date = fifth_week[calendar.WEDNESDAY]
    message='Gli appuntamenti di AUG di questo mese sono:\n Mercoledì %2s e Mercoledì %2s' % (Ameeting_date, Bmeeting_date)
    bot.sendMessage(chat_id=AUGChatId, text=message)
    c = calendar.TextCalendar(calendar.SUNDAY)
    calen=c.formatmonth(year,month)
    calen=calen.replace("  ", "   ")
    calen=calen.replace(" ", " ")
    print(calen)
    bot.sendMessage(chat_id=AUGChatId, text=calen)
    today = datetime.date.today()
    someday = datetime.date(year, month, Ameeting_date)
    diff = someday - today
    message='Più precisamente, mancano %2s giorni al prossimo AUG meeting!!' %(diff.days)
    bot.sendMessage(chat_id=AUGChatId, text=message)


#--------------------------------#
#lists available boards from a json file
def breadboards_list(chat_id):

    filename='tempData/data.json'
    urllib.urlretrieve(DataUrl, filename)

    print filename

    from pprint import pprint
    with open(filename) as jsonFile :
        data = json.load(jsonFile)
    for i in data['breadboard'] :
        print i['name']
        bot.sendMessage(chat_id=chat_id, text="/breadboard_"+i['name'])


#--------------------------------#
#prints images with the thermal printer
def print_breadboard(message, chat_id):

    #filename=wget.download(DataUrl)

    filename='tempdata/data.json'
    urllib.urlretrieve(DataUrl, filename)

    with open(filename) as jsonFile :
        data = json.load(jsonFile)


    for i in data['breadboard'] :
        if i['name'] in message :
            print i['filename']
            #os.remove(i['filename'])

            filename='tempdata/'+i['filename']
            url=GFXUrl+i['filename']
            urllib.urlretrieve(url, filename)

            bot.sendPhoto(chat_id=chat_id, photo=url)

            #filename=wget.download(GFXUrl+i['filename'])
            bot.sendMessage(chat_id=chat_id, text="ok, printing "+message)
            #os.remove(filename)
            return
    bot.sendMessage(chat_id=chat_id, text="Sorry there's no board named "+message)
#--------------------------------#
#main loop - listens for commands.

if __name__ == '__main__':
    while True:
        echo()
        time.sleep(3)
