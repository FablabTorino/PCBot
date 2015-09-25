#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

''' This Bot prints breadboards layout on a thermal printer '''

import telegram
import time
import calendar
import datetime
import string
import json
import urllib

import printer
import privateData

from pprint import pprint


# Telegram Bot Authorization Token
# PCBot
bot = telegram.Bot(privateData.token)
LAST_UPDATE_ID = None
AUGChatId=str(-6549559)

DataUrl="https://raw.githubusercontent.com/FablabTorino/PCBot/master/data/printable.json"
GFXUrl="https://raw.githubusercontent.com/FablabTorino/PCBot/master/gfx/"


class BotCommand:
    command = None
    parameter = None

    def __init__(self, message):
        self.parameter = ""
        cmdSeparator = message.find('_')
        if cmdSeparator != -1:
            self.command = message[:cmdSeparator].strip()
            self.parameter = message[cmdSeparator+1:].strip()
        else:
            parts = message.split(' ')
            self.command = parts[0].strip()
            if len(parts) > 1:
                print self.parameter
                self.parameter = parts[1].strip()


# This will be our global variable to keep the latest update_id when requesting
# for updates. It starts with the latest update_id if available.
try:
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
except IndexError:
    LAST_UPDATE_ID = None


   # custom_keyboard = [[ telegram.Emoji.THUMBS_UP_SIGN,   telegram.Emoji.THUMBS_DOWN_SIGN ]]
   # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
   # bot.sendMessage(chat_id=chat_id, text="Stay here, I'll be back.", reply_markup=reply_markup)

import re
import random


def AUGCalendar(chat_id):
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

    print (message)

    bot.sendMessage(chat_id=chat_id, text=message)

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
#prints images with the thermal printer
def print_breadboard(chat_id, botCmd):
    filename='tempData/data.json'
    urllib.urlretrieve(DataUrl  , filename)

    with open(filename) as jsonFile :
        data = json.load(jsonFile)

    if botCmd.parameter == "list":
        breadboardList = (bread["name"] for bread in data['breadboard'])
        bot.sendMessage(chat_id=chat_id, text='\n'.join(map('/breadboard_{0}'.format, breadboardList)))
        return

    results = {}
    for bread in data['breadboard']:
        if botCmd.parameter in bread["name"]:
            results.update({bread["name"] : bread["filename"]})

    if len(results) == 1:   
        #bot.sendMessage(chat_id=chat_id, text=results.keys()[0])
        #print results.values()[0]
        filename='tempData/' + results.values()[0]
        url=GFXUrl+results.values()[0]
        urllib.urlretrieve(url, filename)

        bot.sendPhoto(chat_id=chat_id, photo=url)
        printer.printImageByUrl(url)
        bot.sendMessage(chat_id=chat_id, text="ok, printing " + botCmd.parameter)
    elif len(results) > 1:
        items = "Sono stati trovati {0} risultati\n".format(len(results))
        items += ('\n'.join(map('/breadboard_{0}'.format, results.keys())))
        bot.sendMessage(chat_id=chat_id, text=items)
    else:
        bot.sendMessage(chat_id=chat_id, text="Nessun risultato per " + botCmd.parameter)


#--------------------------------#
# print pinouts from the thermal printer

def print_pinout(chat_id, botCmd):
    filename='tempData/data.json'
    #urllib.urlretrieve(DataUrl, filename)

    with open(filename) as jsonFile :
        data = json.load(jsonFile)

    results = {}
    categories = data['pinout'].items()
    for category in categories:
        #print 'category name' + category[0]
        for item in category[1]:
            if botCmd.parameter in item['name']:
                results.update({item['name'] : item['filename']})
    print results

    if len(results) == 1:   
        #bot.sendMessage(chat_id=chat_id, text=results.keys()[0])
        #print results.values()[0]
        filename='tempData/' + results.values()[0]
        url=GFXUrl+results.values()[0]
        urllib.urlretrieve(url, filename)

        bot.sendPhoto(chat_id=chat_id, photo=url)
        printer.printImageByUrl(url)
        bot.sendMessage(chat_id=chat_id, text="ok, printing " + botCmd.parameter)
    elif len(results) > 1:
        items = "Sono stati trovati {0} risultati\n".format(len(results))
        items += ('\n'.join(map('/pinout_{0}'.format, results.keys())))
        bot.sendMessage(chat_id=chat_id, text=items)
    else:
        bot.sendMessage(chat_id=chat_id, text="Nessun risultato per " + botCmd.parameter)


    if botCmd.parameter == "list":
        ICList = (pinout["name"] for pinout in data['pinout']['ICs'])
        MicroList = (pinout["name"] for pinout in data['pinout']['Microcontrollers'])
        TransistorsList = (pinout["name"] for pinout in data['pinout']['Transistors'])

        message = 'Available ICs:\n'
        message += '\n'.join(map('/pinout_{0}'.format, ICList))
        message += '\nAvailable Microcontrollers:\n'
        message += '\n'.join(map('/pinout_{0}'.format, MicroList))
        message += '\nAvailable Transistors:\n'
        message += '\n'.join(map('/pinout_{0}'.format, TransistorsList))
        bot.sendMessage(chat_id=chat_id, text=message)
        return


def print_url(chat_id, botCmd):
    imageTypes = ['.jpg', '.png', '.jpeg']
    if any(x in botCmd.parameter for x in imageTypes):
        print ("I'm printing an image")
        printer.printImageByUrl(botCmd.parameter)
    else:
        print ("this is not an image")    


def help(chat_id, botCmd):
    bot.sendMessage(chat_id=chat_id, text='\n'.join(commands.keys()))


commands = {
    '/help' : help,
    '/AUGCalendar' : AUGCalendar,
    '/breadboard': print_breadboard,
    '/pinout': print_pinout,
    '/print' : print_url
}


def setup():
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
        print LAST_UPDATE_ID
    except IndexError:
        LAST_UPDATE_ID = None


def parseMessage(update):
    message = update.message.text
    chat_id = update.message.chat_id
    if message.startswith('/'):
        botCmd = BotCommand(message)

        if botCmd.command in commands:
            commands[botCmd.command](chat_id, botCmd)
        else:
            bot.sendMessage(chat_id=chat_id, text='Invalid command')

    else:
        print "MESSAGE " + message


#--------------------------------#
#main loop - listens for commands.

if __name__ == '__main__':
    setup()

    while True:
        try:
            for update in bot.getUpdates(offset=LAST_UPDATE_ID):
                if LAST_UPDATE_ID < update.update_id:
                    LAST_UPDATE_ID = update.update_id
                    chat_id = update.message.chat_id
                    from_user = update.message.from_user
                    if update.message.text:
                        parseMessage(update)

        except:
            pass
        time.sleep(0.5)
