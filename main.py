import requests
import time
import re
import json
import os



id_list = []
date_list = []
api_key = "moby_YXyzhJMmxrbwCTmUy5TfnLUfQu5"

if os.path.isfile("api_calls.txt") == True:
    if os.path.getsize("api_calls.txt") != 0:
        file = open("api_calls.txt","r")
        api_calls = file.readline()
        api_calls = int(api_calls)
    else:
        file = open("api_calls.txt","w")
        file.write("0")
        file.close()
        file = open("api_calls","r")
        api_calls = file.readline()

##########

def get_id(title):
    url = "https://api.mobygames.com/v1/games"
    params = {"api_key":api_key,"title":title,"format":"id"}

    response = requests.get(url, params)
    time.sleep(1)
    global api_calls
    api_calls += 1

    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print("Error Code: " + str(response.status_code))

def get_date(id):
    url = "https://api.mobygames.com/v1/games/" + str(id) + "/platforms"
    params = {"api_key":api_key}
    response = requests.get(url, params)
    time.sleep(1)
    global api_calls
    api_calls += 1
    if response.status_code == 200:
        return response.json()
    else:
        print("Error Code: " + str(response.status_code))

##########

def extract_id(data):
    for value in data.values():
        return value

def extract_date(data):
    data = str(data)
    date = re.findall(r'\d{4}', data)
    return date

##########

def make_id_list(value):
    id_list.append(value)
    print(id_list)

def make_date_list(value):
    date_list.append(value)
    print(date_list)

##########

def write_id_list(name):
    file = open(name,"w")
    for i in id_list:
        file.write(str(i)+"\n")
    file.close()

def write_date_list(name):
    file = open(name,"w")
    for d in date_list:
        file.write(str(d)+"\n")
    file.close()

##########

def create_id_list(titles, name):
    for t in titles:
        make_id_list(extract_id(get_id(t)))
        time.sleep(1)
    
    write_id_list(name)

def create_date_list(ids, name):
    game_current = 0
    game_count = len(ids)
    for line in ids:
        game_current += 1
        list = line.strip('][').split(', ')
        date_list = []
        print("Game " + str(game_current) + "/" + str(game_count))
        for id in list:
            date = extract_date(get_date(id))
            for d in date:
                d = int(d)
                if d >= 1980:
                    date_list.append(d)
        final_date = min(date_list)
        make_date_list(final_date)
    
    write_date_list(name)

def menu():
    menu = True
    while menu == True:
        print("Would you like to:")
        print("1. Load List of Game Titles and Create ID List")
        print("2. Load ID List and Create Date List")
        print("3. Enter Game Title Manually and Get First Release Date")
        print("4. Exit Program")
        choice = input()
        if choice == "1":
            name = input("Enter the name of the titles text file: ")
            id_name = input("Name the output file (remember to include .txt): ")
            with open(name) as x:
                titles = x.read().splitlines()
            create_id_list(titles, id_name)
            menu = False
        elif choice == "2":
            name = input("Enter the name of the ID List text file: ")
            date_name = input("Name the output file (remember to include .txt): ")
            with open(name) as y:
                ids = y.read().splitlines()
            create_date_list(ids, date_name)
            menu = False
        elif choice == "3":
            game_title = input("Enter the title of the game (not case sensitive): ")
            id_list = extract_id(get_id(game_title))
            total_time = len(id_list)
            date_list = []
            if len(id_list) > 0:
                for id in id_list:
                    date = extract_date(get_date(id))
                    os.system("cls")
                    total_time -= 1
                    print("Time Remaining: " + str(total_time))
                    for d in date:
                        d = int(d)
                        if d >= 1980:
                            date_list.append(d)
                final_date = min(date_list)
                os.system("cls")
                print(game_title + " was first released in " + str(final_date))
                print()
                print("Total API Calls Made: " + str(api_calls))
                print()
        elif choice == "4":
            menu = False
        else:
            print("Invalid Input!")         
        
menu()

file = open("api_calls.txt","w")
file.write(str(api_calls))
file.close()

## good human to computer interaction

## countdown

## 360 api call limit

## robust exception handling