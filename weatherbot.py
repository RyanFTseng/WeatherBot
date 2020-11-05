# -*- coding: utf-8 -*-
from tkinter import *
import queue
import requests
import sys
import random

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
    tmpMsg = message.replace('?','')
    tmpMsg = tmpMsg.replace('.','')
    tmpMsg = tmpMsg.replace('!', '')
    tmpMsg = tmpMsg.replace(',', '')
    wordList = tmpMsg.split()

    for v, w in zip(wordList[:-1], wordList[1:]): # takes two words in the list and puts them into a single string
        # which is run through get_weather
        tmp = v + ' ' + w
        weather = get_weather(api_key, tmp)
        # checks if user input is valid
        if (str(weather['cod']) == '404'):
            continue
        else:
            city = tmp
            return

    for x in wordList:
        weather = get_weather(api_key, x)
        if (str(weather['cod']) == '404'):
            continue
        else:
            city = x
            return

def return_weather():
    try: # fails if city is not initialized or temperature call fails
        window.insert(END, 'The temperature in ' + city + ' is currently ' + str(weather['main']['temp'])
                      + '°C' + '\n') # obtains the temperature in city and shows it. str converts a part
        # of a dictionary to a string
        window.insert(END, 'The weather in ' + city + ' is currently ' + str(weather["weather"][0]["main"]) + '\n')
        # obtains weather condition in city and shows it
        window.configure(state="disabled")
        get_clothing_options()
        return
    except: # takes reply of user
        reply = random.choice(replies)
        window.insert(END, reply)
        window.insert(END, '\n')
        window.configure(state="disabled")
        return

def write_window(): # writes user input to the messages
    global message
    window.configure(state="normal")
    message = e1.get()
    window.insert(END, message) # writes user input to the messages
    window.insert(END, '\n')
    e1.delete(0, len(message))
    parse_response()
    return_weather()
    return

def get_clothing_options(): # checks the weather and temperature to determine what the user should wear
    window.configure(state="normal") # makes it so the user interface will show the clothing options
    if str(weather["weather"][0]["main"]) == "Thunderstorm" or str(weather["weather"][0]["main"]) == "Drizzle" or str(weather["weather"][0]["main"]) == "Rain":
        window.insert(END, 'Bring an umbrella and a rain coat' + '\n')
    elif str(weather["weather"][0]["main"]) == "Snow":
        window.insert(END, 'Wear a snowsuit' + '\n')

    if weather['main']['temp'] > 0 and weather['main']['temp'] < 15:
        window.insert(END, 'Wear a jacket with long sleeves and pants' + '\n')
    elif weather['main']['temp'] > 15 and weather['main']['temp'] < 25:
        window.insert(END, 'Clothing can be lighter' + '\n')
    elif weather['main']['temp'] > 25:
        window.insert(END, 'Wear short sleeves and shorts, maybe with a hat' + '\n')
    return

def get_weather(api_key, location): # how the program can access the weather api to get the weather
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
# creates the text box and the button, and makesthe user input be checked
e1 = Entry(master, width=85)
b1 = Button(master, text='send', command=write_window).pack(side=RIGHT)
e1.pack(side=RIGHT)

master.mainloop()

