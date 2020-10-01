import re
import bs4
import queue
import json
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
from datetime import datetime
import time

INDEX_IGNORE = set(['marcussen', 'du', 'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there',
        'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 
    'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 
    's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 
    'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 
    'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 
    'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 
    'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now',
     'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 
     'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 
     'it', 'how', 'further', 'was', 'here', 'than', 'u', 'like', 'oh', "it's" "i'm", "i’m", "also", "it's",
     "get", "r"])
'''
Cleaning file to get raw data we want
'''
file = open("message_1.html")
soup = bs4.BeautifulSoup(file)

names = soup.find_all("div", class_="_3-96 _2pio _2lek _2lel") #name
datetimes = soup.find_all("div", class_="_3-94 _2lem") # date
contents = soup.find_all("div", class_="_3-96 _2let") # content

name_text = []
for name in names:
    name_text.append(name.text)

content_text = []
for content in contents:
    content_text.append(content.text.lower())

dates = []
times = []
dates_list = []
times_list = []
for datetimer in datetimes:
    dnt = datetimer.text.rsplit(",", 1)
    date = datetime.strptime(dnt[0], "%b %d, %Y").strftime("%Y-%m-%d")
    timer = datetime.strptime(dnt[1][1:], "%I:%M %p").strftime("%H:%M")
    dates.append(date)
    if date not in dates_list:
        dates_list.append(date)
    times.append(timer)
    if timer not in times_list:
        times_list.append(timer)

'''
Making our dataframes
'''
textcols = {"Sender": name_text, "Date": dates, "Time": times, "Contents": content_text}
rawtext_df = pd.DataFrame(textcols)
rawtext_df.sort_values(by=['Date'])

blank_date_list = [None] * len(dates_list)
blank_time_list = [None] * len(times_list)

blank_date_df = pd.DataFrame({"Sender": blank_date_list, "Date": dates_list, "Time": blank_date_list})
blank_time_df = pd.DataFrame({"Sender": blank_time_list, "Date": blank_time_list, "Time": times_list})

word_dates = []
word_times = []
word_names = []
word_list = []
num_words_total = 0
for i in range(0, len(content_text)):
    words = content_text[i].split()
    for word in words:
        num_words_total += 1
        if word not in INDEX_IGNORE:
            word_list.append(word)
            word_dates.append(dates[i])
            word_times.append(times[i])
            word_names.append(name_text[i])

print("Num words total: " + str(num_words_total))
print("Average words per message:" + str(num_words_total/len(content_text)))
print("Num messages total: " + str(len(content_text)))

print("Messages sent by Christie: " + str(rawtext_df.loc[rawtext_df["Sender"] == "Christie Du"].size/4))
print("Messages sent by Max: " + str(rawtext_df.loc[rawtext_df["Sender"] == "Max Marcussen"].size/4))

wordcols = {"Sender": word_names, "Date": word_dates, "Time": word_times, "Word": word_list}
word_df = pd.DataFrame(wordcols)
word_df.sort_values(by=['Date'])

blank_word = [None] * len(word_list)

blank_word_df = pd.DataFrame({"Sender": blank_word, "Date": word_dates, "Time": word_times, "Word": blank_word})


print("Non-stopwords sent by Christie: " + str(word_df.loc[word_df["Sender"] == "Christie Du"].size/4))
print("Non-stopwords sent by Max: " + str(word_df.loc[word_df["Sender"] == "Max Marcussen"].size/4))

#text date plot - outputs plot of texting days plus top 10 texting days
wordrank = word_df["Word"].value_counts(sort=True)
print("Top 30 words sent:")
print(wordrank.head(n=30))

rawtext_textrank = rawtext_df["Contents"].value_counts(sort=True)
print("Top 30 messages sent:")
print(rawtext_textrank.head(n=30))


# make day rank series
word_dayrank = word_df["Date"].value_counts(sort=True)
print("10 days with most words sent:")
print(word_dayrank.head(n=10))
word_dayrank = word_dayrank.sort_index()

rawtext_dayrank = rawtext_df["Date"].value_counts(sort=True)
print("10 days with most messages sent:")
print(rawtext_dayrank.head(n=10))
rawtext_dayrank = rawtext_dayrank.sort_index()

def put_to_csv():
    word_df.to_csv("word_sheet.csv")

def freq_charts():
    #then plot them
    # plot of days vs. frequency
    plt.figure(figsize=(12, 5))
    plt.xlabel("Date")
    plt.ylabel("Number")
    ax1 = word_dayrank.plot(color='blue', grid=True, label='Word count')
    ax2 = rawtext_dayrank.plot(color='red', grid=True, secondary_y=True, label='Message count')
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    plt.legend(h1+h2, l1+l2, loc=2)
    plt.show()

    #plot of time of day vs. frequency
    word_timerank = word_df["Time"].value_counts().sort_index()
    print(type(word_timerank[0]))
    rawtext_timerank = rawtext_df["Time"].value_counts().sort_index()
    plt.figure(figsize=(12, 5))
    plt.xlabel("Time of Day")
    plt.ylabel("Number")
    ax1 = word_timerank.plot(color='blue', grid=True, label='Word count')
    ax2 = rawtext_timerank.plot(color='red', grid=True, secondary_y=True, label='Message count')
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    plt.legend(h1+h2, l1+l2, loc=2)
    plt.show()


'''
Plot of usage of certain words over time
'''


def find_word_freq(word, timetype="Date", by_person=False):
    '''
    gives frequency of certain non-stopword over time.
    '''

    if by_person:
        person1df = word_df.loc[word_df["Sender"] == "Christie Du"].loc[word_df["Word"].str.contains(word)]
        person2df = word_df.loc[word_df["Sender"] == "Max Marcussen"].loc[word_df["Word"].str.contains(word)]
        if timetype == "Date":
            person1df = pd.concat([person1df, blank_date_df], sort=True)
            person2df = pd.concat([person2df, blank_date_df], sort=True)
            p1rank = person1df["Date"].value_counts().sort_index() -1
            p2rank = person2df["Date"].value_counts().sort_index() -1
        else:
            person1df = pd.concat([person1df, blank_time_df], sort=True)
            person2df = pd.concat([person2df, blank_time_df], sort=True)
            p1rank = person1df["Time"].value_counts().sort_index() -1
            p2rank = person2df["Time"].value_counts().sort_index() -1
        plt.figure(figsize=(12, 5))
        plt.xlabel(timetype)
        plt.ylabel(word + " count")
        ax1 = p1rank.plot(color='red', grid=True, label='Christie')
        ax2 = p2rank.plot(color='green', grid=True, secondary_y=True, label='Max')
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        plt.legend(h1+h2, l1+l2, loc=2)
        plt.title("Use of word " + word + " vs. " + timetype)
        plt.show()
    else:
        specialdf = word_df.loc[word_df["Word"].str.contains(word)]
        if timetype == "Date":
            specialdf = pd.concat([specialdf, blank_date_df], sort=True)
            specialdf_dayrank = specialdf["Date"].value_counts().sort_index() - 1
        else:
            specialdf = pd.concat([specialdf, blank_time_df], sort=True)
            specialdf_dayrank = specialdf["Time"].value_counts().sort_index() - 1
        specialdf_dayrank.plot(title="Uses of word " + word + " vs. " + timetype)
        plt.title("Use of word " + word + " vs. " + timetype)
        plt.show()

def find_message_freq(message, timetype="Date"):
    '''
    finds frequency of message.
    '''
    specialdf = rawtext_df.loc[rawtext_df["Contents"] == message]
    if timetype == "Date":
        specialdf_dayrank = specialdf["Date"].value_counts().sort_index()
    else:
        specialdf_dayrank = specialdf["Time"].value_counts().sort_index()
    specialdf_dayrank.plot(title="Sends of message " + message + " vs. date")
    plt.show()

def find_person_freq(kind="message", timetype="Date"):
    '''
    gives graph of people's words and messages over time.
    '''
    if kind=="message":
        person1df = rawtext_df.loc[rawtext_df["Sender"] == "Christie Du"]
        person2df = rawtext_df.loc[rawtext_df["Sender"] == "Max Marcussen"]
    else:
        person1df = word_df.loc[word_df["Sender"] == "Christie Du"]
        person2df = word_df.loc[word_df["Sender"] == "Max Marcussen"]
    if timetype == "Date":
        p1rank = person1df["Date"].value_counts().sort_index()
        p2rank = person2df["Date"].value_counts().sort_index()
    else:
        p1rank = person1df["Time"].value_counts().sort_index()
        p2rank = person2df["Time"].value_counts().sort_index()
    plt.figure(figsize=(12, 5))
    plt.xlabel(timetype)
    plt.ylabel(kind + " count")
    ax1 = p1rank.plot(color='red', grid=True, label='Christie')
    ax2 = p2rank.plot(color='green', grid=True, secondary_y=True, label='Max')
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    plt.legend(h1+h2, l1+l2, loc=2)
    plt.show()

def run_all():
    freq_charts()
    find_person_freq()
    find_person_freq("word", "Date")
    find_person_freq("message", "Time")
    find_person_freq("word", "Time")
    find_word_freq("love", "Date")
    find_word_freq("love", "Date", True)
    find_word_freq("love", "Time")
    find_word_freq("love", "Time", True)
    find_word_freq("fuck", "Time")
    find_word_freq("fuck", "Date")
    find_word_freq("fuck", "Date", True)
    find_word_freq("bub", "Date")
    find_word_freq("bub", "Date", True)
    find_word_freq("bub", "Time", True)
    find_word_freq("dude", "Date", True)
    find_word_freq("lmao", "Date")
    find_word_freq("lmao", "Date", True)
    find_word_freq("lmao", "Time")
    find_word_freq("call", "Date")
    find_word_freq("call", "Time")
    find_word_freq("😍", "Date", True)
    find_word_freq("😍", "Time", True)
    find_word_freq("😍christie", "Date")
    find_word_freq("😍christie", "Time")
    find_word_freq("😍max", "Date")
    find_word_freq("😍max", "Time")
    find_word_freq("👉", "Date", "True")