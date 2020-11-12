# -*- coding: utf-8 -*-
from tkinter import *
import requests
import random
import re
import datetime

api_key = "ee6312fae267795f645312a00f90f4d3"
lat = "48.208176"
lon = "16.373819"
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
# Below are some replies for if the user types anything other than the name of a real city
replies = ['Please type in a valid name of the city you want the weather of.',
           'Is that even a city?',
           'Hello? Do you know how to type?',
           'Hey I am looking for city names not whatever you typed.',
           'Congratulations, you invented a city!',
           'If you look hard enough, you will see that there are letters on your keyboard.',
           ''
           ]


def parse_response():
    global weather
    global city
    # the four below lines remove certain punctuation from the user input
    tmpMsg = message.replace('?', '')
    tmpMsg = tmpMsg.replace('.', '')
    tmpMsg = tmpMsg.replace('!', '')
    tmpMsg = tmpMsg.replace(',', '')
    wordList = tmpMsg.split()

    for v, w in zip(wordList[:-1], wordList[1:]):  # takes two words in the list and puts them into a single string
        # which is run through get_weather
        tmp = v + ' ' + w
        weather = get_weather(api_key, tmp)
        # checks if user input is valid
        if str(weather['cod']) == '404':
            continue
        else:
            city = tmp
            extract_time()
            return

    for x in wordList:
        weather = get_weather(api_key, x)
        if str(weather['cod']) == '404':
            continue
        else:
            city = x
            extract_time()
            return

def extract_time():
    global timeweather # Will be used in case the method fails, then the bot can still extract the weather for the
    # default time
    global timedate # Will be used if the user specifies a specific time and date in the bot's response
    global foundtime # This is here so the bot will know to add timedate in its response
    global year # Will be the first parameter for fetching the unix version of the time
    global month # Will be the second parameter for fetching the unix version of the time
    global day # Will be the third parameter for fetching the unix version of the time
    global hour # Will be the fourth parameter for fetching the unix version of the time
    global minute # Will be the fifth parameter for fetching the unix version of the time
    foundtime = 0
    stringmessage = message
    # This is how the bot extracts time
    dateregex = r"(\d{4})/(\d{1,2})/(\d{1,2})" # The bot will be able to determine a specific date
    timeregex = r"(\d{1,2}):(\d{2})" # The bot will be able to determine a specific time
    datematch = re.search(dateregex, message)
    timematch = re.search(timeregex, message)
    if not datematch and not timematch:
        return
    if datematch:
        yearstring = datematch.group(1)
        year = int(yearstring)
        monthstring = datematch.group(2)
        month = int(monthstring)
        if month < 1: # Month is set to January if the month is less than 1
            month = 1
        elif month > 12: # Month is set to December if the month is greater than 12
            month = 12
        monthstring = str(month)
        daystring = datematch.group(3)
        day = int(daystring)
        if day < 1: # If the day is less than 1, it is defaulted to 1
            day = 1
        # If the day is greater than 31 and the month has 31 days, it is defaulted to 31
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            if day > 31:
                day = 31
        # If the day is greater than 30 and the month has 30 days, it is defaulted to 30
        elif month == 4 or month == 6 or month == 9 or month == 11:
            if day > 30:
                day = 30
        elif month == 2:
            # If the year is not a leap year, the month is February, and the day is greater than 28, it is
            # defaulted to 28.
            # If the year is a leap year, the month is February, and the day is greater than 29, it is defaulted
            # to 29
            if year % 4 != 0 and day > 28:
                day = 28
            elif year % 4 == 0:
                if year % 100 != 0 and day > 29:
                    day = 29
                # If a year is at the end of a century, it will only be a leap year if it goes into 400,
                # which is why we needed more calculations for years that go into 4.
                elif year % 100 == 0:
                    if year % 400 != 0 and day > 28:
                        day = 28
                    elif year % 400 == 0 and day > 29:
                        day = 29
        daystring = str(day)
        timedate = yearstring + '/' + monthstring + '/' + daystring
        if not timematch: # If the user did not specify a time
            hour = 0
            minute = 0
        foundtime = 1
    if timematch:
        hourstring = timematch.group(1)
        hour = int(hourstring)
        # If the hours are less than 0, they are defaulted to 0
        if hour < 0:
            hour = 0
        # If the hours are greater than 23, they are defaulted to 23
        elif hour > 23:
            hour = 23
        hourstring = str(hour)
        minutestring = timematch.group(2)
        minute = int(minutestring)
        # If the minutes are less than 0, they are set to 0
        if minute < 0:
            minute = 0
        # If the minutes are greater than 59, they are set to 59
        elif minute > 59:
            minute = 59
        minutestring = str(minute)
        if datematch: # If the user specified a date
            timedate = timedate + ', ' + hourstring + ':' + minutestring
        else: # If the user did not specify a date
            timedate = hourstring + ':' + minutestring
            y = datetime.datetime.now()
            year = y.year
            month = y.month
            day = y.day
        foundtime = 1
    try:
        dt = datetime.datetime(year, month, day, hour, minute)
        timestamp = int((dt - datetime.datetime(1970, 1, 1)).total_seconds())
        timeweather = get_timeweather(api_key, timestamp, city)
        return
    except Exception as ex:
        return

def get_timeweather(api_key, timestamp, location):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&dt={}&units=metric&appid={}".format(location,
    timestamp, api_key,)
    r = requests.get(url)
    return r.json()

def return_weather():
    global foundtime # Because foundtime is defined again here, it has to once again be declared global
    if foundtime == 1:
        try:
            window.insert(END, 'The temperature in ' + city + ' at ' + timedate + ' will be ' +
                          str(timeweather['main']['temp']) + '°C' + '\n')
            window.insert(END, 'The weather in ' + city + ' at ' + timedate + ' will be ' +
                          str(timeweather["weather"][0]["main"]) + '\n')
            returneddt = timeweather['dt']
            window.insert(END, 'The returned time is ' + str(datetime.datetime.fromtimestamp(returneddt)) + '\n')
            foundtime = 0
            window.configure(state="disabled")
            get_clothing_options()
            return
        except:
            reply = random.choice(replies)
            window.insert(END, reply)
            window.insert(END, '\n')
            window.configure(state="disabled")
            foundtime = 0
            return
    else:
        try:  # fails if city is not initialized or temperature call fails
            window.insert(END, 'The temperature in ' + city + ' is currently ' + str(weather['main']['temp'])
                          + '°C' + '\n')  # obtains the temperature in city and shows it. str converts a part
            # of a dictionary to a string
            window.insert(END, 'The weather in ' + city + ' is currently ' + str(weather["weather"][0]["main"]) + '\n')
            # obtains weather condition in city and shows it
            window.configure(state="disabled")
            get_clothing_options()
            return
        except:  # takes reply of user
            reply = random.choice(replies)
            window.insert(END, reply)
            window.insert(END, '\n')
            window.configure(state="disabled")
            return

def write_window():  # writes user input to the messages
    global message
    window.configure(state="normal")
    message = e1.get()
    window.insert(END, message)  # writes user input to the messages
    window.insert(END, '\n')
    e1.delete(0, len(message))
    parse_response()
    return_weather()
    return


def get_clothing_options():  # checks the weather and temperature to determine what the user should wear
    window.configure(state="normal")  # makes it so the user interface will show the clothing options
    if str(weather["weather"][0]["main"]) == "Thunderstorm" or str(weather["weather"][0]["main"]) == "Drizzle" or str(
            weather["weather"][0]["main"]) == "Rain":
        window.insert(END, 'Bring an umbrella and a rain coat' + '\n')
    elif str(weather["weather"][0]["main"]) == "Snow":
        window.insert(END, 'Wear a snowsuit' + '\n')

    if 0 < weather['main']['temp'] < 15:
        window.insert(END, 'Wear a jacket with long sleeves and pants' + '\n')
    elif 15 < weather['main']['temp'] < 25:
        window.insert(END, 'Clothing can be lighter' + '\n')
    elif weather['main']['temp'] > 25:
        window.insert(END, 'Wear short sleeves and shorts, maybe with a hat' + '\n')
    return


def get_weather(api_key, location):  # how the program can access the weather api to get the weather
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, api_key)
    r = requests.get(url)
    return r.json()


master = Tk()
# when the window opens, the bot asks the user what city they want to know the weather of
window = Text(master)
window.insert(END, 'Hi! What city do you want the weather of right now?')
window.insert(END, '\n')
window.configure(state="disabled")
window.pack()
# creates the text box and the button, and makes the user input be checked
e1 = Entry(master, width=85)
b1 = Button(master, text='send', command=write_window).pack(side=RIGHT)
e1.pack(side=RIGHT)

master.mainloop()
