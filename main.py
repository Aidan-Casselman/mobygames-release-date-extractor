import requests
import time
import re
import os
from datetime import datetime, timedelta

# MobyGames Release Date Extractor
# Version 1.0

# save.txt explanation:
# 0 = api_key
# 1 = datetime
# 2 = api_calls
# 3 = min_date
# 4 = limit
# 5 = True = Latest Release Date; False(default) = First Release Date

id_list = []
date_list = []

now_time = datetime.now()

if os.path.isfile("save.txt") == True:
    file = open("save.txt","r")
    lines = file.read().splitlines()
    api_key = lines[0]
    launch_time = lines[1]
    launch_time = datetime.strptime(launch_time, '%Y-%m-%d %H:%M:%S.%f')
    difference = now_time - launch_time
    threshold = timedelta(hours = 1)
    if difference >= threshold:
        api_calls = 0
        launch_time = now_time
    else:
        api_calls = lines[2]
        api_calls = int(api_calls)
    min_date = lines[3]
    min_date = int(min_date)
    limit = lines[4]
    limit = int(limit)
    last_release = lines[5]
    last_release = bool(last_release)
else:
    key = input("Please enter a valid MobyGames.com API Key: ")
    print("Welcome!")
    file = open("save.txt","w")
    file.write(str(key)+"\n")
    file.write(str(now_time)+"\n")
    file.write("0\n")
    file.write("1948\n")
    file.write("100\n")
    file.write("False\n")
    file.close()
    api_key = key
    api_calls = 0
    launch_time = now_time
    min_date = 1948
    limit = 100
    last_release = False

##########

def get_id(title):
    url = "https://api.mobygames.com/v1/games"
    words = title.split()
    if words[0] == "the" or words[0] == "The":
        title = title[4:]
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
    print(value)

def make_date_list(value):
    date_list.append(value)
    print(value)

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
    write_id_list(name)

def create_date_list(ids, name):
    game_current = 0
    game_count = len(ids)
    id_count = 0
    for line in ids:
        list = line.strip('][').split(', ')
        for id in list:
            id_count += 1
    check = take_user_input("There are " + str(id_count) + " IDs, meaning this will take " + str(id_count) + " API calls to complete. Do you wish to continue? (y/n): ")
    if check == "y":
        for line in ids:
            game_current += 1
            list = line.strip('][').split(', ')
            date_list = []
            print("Game " + str(game_current) + "/" + str(game_count))
            for id in list:
                date = extract_date(get_date(id))
                for d in date:
                    d = int(d)
                    if d >= min_date:
                        date_list.append(d)
            if last_release == False:
                final_date = min(date_list)
            else:
                final_date = max(date_list)
            make_date_list(final_date)
        
        write_date_list(name)
        print()
        print("Done. Saved to " + name)
        print()

def save():
    file = open("save.txt","w")
    file.write(api_key + '\n')
    file.write(str(launch_time) + '\n')
    file.write(str(api_calls) + '\n')
    file.write(str(min_date) + '\n')
    file.write(str(limit) + '\n')
    file.write(str(last_release) + '\n')

def remove_menu(lines):
    delete = lines
    while delete > 0:
        print ("\033[A                                                                           \033[A")
        delete -= 1

def take_user_input(message):
    repeat = True
    while repeat == True:
        string = input(message)
        if string:
            return string.strip()
        else:
            print("Invalid Input!")

def menu():
    global api_key
    global min_date
    global limit
    global last_release
    menu = True
    while menu == True:
        print("Would you like to:")
        print("1. Load List of Game Titles and Create ID List")
        print("2. Load ID List and Create Date List")
        print("3. Enter Game Title Manually and Get First Release Date")
        print("4. Settings")
        print("5. Exit Program")
        choice = take_user_input("")
        if choice == "1":
            remove_menu(7)
            name = take_user_input("Enter the name of the titles text file: ")
            id_name = take_user_input("Name the output file (remember to include .txt): ")
            with open(name) as x:
                titles = x.read().splitlines()
            create_id_list(titles, id_name)
        elif choice == "2":
            remove_menu(7)
            name = take_user_input("Enter the name of the ID List text file: ")
            date_name = take_user_input("Name the output file (remember to include .txt): ")
            with open(name) as y:
                ids = y.read().splitlines()
            create_date_list(ids, date_name)
        elif choice == "3":
            remove_menu(7)
            game_title = take_user_input("Enter the title of the game (not case sensitive): ")
            print("Searching...")
            id_list = extract_id(get_id(game_title))
            total_time = len(id_list)
            if total_time < 1:
                print("Game not found!")
            else:
                if total_time == 100:
                    choice = take_user_input("There are " + str(total_time) + " (limit 100) Game IDs matching " + str(game_title) + ". Would you like to continue? (y/n): ")
                else:
                    choice = take_user_input("There are " + str(total_time) + " Game IDs matching " + str(game_title) + ". Would you like to continue? (y/n): ")
                if choice == "y":
                    print ("\033[A                                                                                                                        \033[A")
                    print("Game IDs Remaining: " + str(total_time))
                    date_list = []
                    if len(id_list) > 0:
                        for id in id_list:
                            date = extract_date(get_date(id))
                            print ("\033[A                                                                                                                        \033[A")
                            total_time -= 1
                            print("Game IDs Remaining: " + str(total_time))
                            for d in date:
                                d = int(d)
                                if d >= min_date:
                                    date_list.append(d)
                        if last_release == False:
                            final_date = min(date_list)
                            print ("\033[A                             \033[A")
                            print()
                            print(game_title + " was first released in " + str(final_date))
                        else:
                            final_date = max(date_list)
                            print ("\033[A                             \033[A")
                            print()
                            print(game_title + " was last released in " + str(final_date))
                        print()
                        print("API Calls Made Within Hour: " + str(api_calls) + "/360")
                        print()
        elif choice == "4":
            remove_menu(7)
            file = open("save.txt","r")
            lines = file.read().splitlines()
            print("1. api_key = " + str(lines[0]))
            print("2. Minimum Date = " + str(lines[3]))
            print("3. Limit = " + str(lines[4]))
            print("4. Latest Release Date = " + str(lines[5]))
            print("5. Go Back to Menu")
            choice = take_user_input("")
            if choice == "1":
                remove_menu(6)
                key = take_user_input("Enter new api key: ")
                api_key = key
                save()
            elif choice == "2":
                remove_menu(6)
                date = take_user_input("Enter new minimum year: ")
                min_date = int(date)
                save()
            elif choice == "3":
                remove_menu(6)
                new_limit = take_user_input("Enter new limit (max 100): ")
                new_limit = int(new_limit)
                if new_limit > 100:
                    new_limit = 100
                limit = new_limit
                save()
            elif choice == "4":
                remove_menu(6)
                release = take_user_input("Would you like to search for latest release instead of first release? (y/n): ")
                if release == "y":
                    last_release = True
                    save()
                elif release == "n":
                    last_release = False
                    save()
            elif choice == "5":
                remove_menu(6)

        elif choice == "5":
            menu = False
        else:
            print("Invalid Input!")
        save()     
        
menu()