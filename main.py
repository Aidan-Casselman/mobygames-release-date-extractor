import requests
import time
import csv
import os
import html
from datetime import datetime, timedelta

# MobyGames Release Date Extractor
# Version 1.0

# save.txt explanation:
# 0 = api_key
# 1 = datetime
# 2 = api_calls
# 3 = limit
# 4 = exact_query_match
# 5 = year_only

# initializes variables and reads save file on launch
def initialize():
    now_time = datetime.now()
    os.system("")
    global api_key, api_calls, launch_time, limit, exact_query_match, year_only

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
        limit = lines[3]
        limit = int(limit)
        exact_query_match = lines[4].lower() == 'true'
        exact_query_match = bool(exact_query_match)
        year_only = lines[5].lower() == 'true'
        year_only = bool(year_only)
    else:
        key = input("Please enter a valid MobyGames.com API Key: ")
        print("Welcome!")
        file = open("save.txt","w")
        file.write(str(key)+"\n")
        file.write(str(now_time)+"\n")
        file.write("0\n")
        file.write("100\n")
        file.write("False\n")
        file.write("False\n")
        file.close()
        api_key = key
        api_calls = 0
        launch_time = now_time
        limit = 100
        exact_query_match = False
        year_only = False

# queries MobyGames API to retrieve game data based on given title
def get_data(title):
    url = "https://api.mobygames.com/v1/games"
    words = title.split()
    if words[0] == "the" or words[0] == "The":
        title = title[4:]
    params = {"api_key":api_key,"title":title,"format":"normal","limit":limit}

    response = requests.get(url, params)
    time.sleep(1)
    global api_calls
    api_calls += 1

    if response.status_code == 200:
        data = response.json()
        return(data)
    elif response.status_code == 400:
        print("Error code: " + str(response.status_code))
        print("Your query could not be processed, possibly due to invalid parameter types, e.g. a string where an integer was expected.")
    elif response.status_code == 401:
        print("Error code: " + str(response.status_code))
        print("You attempted to access an endpoint without providing a valid API key.")
    elif response.status_code == 404:
        print("Error code: " + str(response.status_code))
        print("You attempted to access an object that does not exist.")
    elif response.status_code == 422:
        print("Error code: " + str(response.status_code))
        print("The value of some parameter was of the right type, but was invalid.")
    elif response.status_code == 429:
        pause()
    else:
        print("Error Code: " + str(response.status_code))

# extracts and formats release dates
def extract_dates(game):
    title = game.get('title')
    release_dates = {}
    global year_only
    for platform in game.get('platforms', []):
        platform_name = platform.get('platform_name')
        release_date = platform.get('first_release_date')
        if (year_only == True) & (len(release_date) > 4):
            release_date = release_date[:-6]
        if platform_name and release_date:
            release_dates[platform_name] = release_date
    return ({'title': title, 'release_dates': release_dates})

# extracts information for each game
def extract_game_info(data, game_title):
    games_info = []
    global exact_query_match
    for game in data.get('games', []):
        if exact_query_match == True:
            if (game.get('title').lower() == game_title.lower()):
                games_info.append(extract_dates(game))
        else:
            games_info.append(extract_dates(game))
    return games_info

# writes the list of dates to a text file
def write_date_list(list, name):
    file = open(name,"w")
    for d in list:
        file.write(str(d)+"\n")
    file.close()

# searches and returns the release date of a game for the specified platform
def get_release_date_for_platform(game_info, platform_name):
    for game in game_info:
        for platform, release_date in game['release_dates'].items():
            platform = platform.lower()
            platform_name = platform_name.lower()
            platform_mapping = {
                '2600': 'atari 2600',
                2600: 'atari 2600',
                'c64': 'commodore 64',
                'dc': 'dreamcast',
                'gb': 'game boy',
                'gba': 'game boy advance',
                'gbc': 'game boy color',
                'gg': 'game gear',
                'gc': 'gamecube',
                'gen': 'genesis',
                'ng': 'neo geo',
                '3ds': 'nintendo 3ds',
                'n64': 'nintendo 64',
                'ds': 'nintendo ds',
                'dsi': 'nintendo dsi',
                'ps': 'playstation',
                'ps2': 'playstation 2',
                'ps3': 'playstation 3',
                'ps4': 'playstation 4',
                'ps5': 'playstation 5',
                'psv': 'ps vita',
                'sat': 'sega saturn',
                'tg16': 'turbografx-16',
                'pc': 'windows',
                'ws': 'wonderswan',
                'wiiu': 'wii u',
                'xb': 'xbox',
                'x360': 'xbox 360',
                'xb360': 'xbox 360',
                'xb1': 'xbox one',
                'xbone': 'xbox one',
                'xone': 'xbox one',
                'xbs': 'xbox series',
                'xbox series x': 'xbox series',
                'xbox series s': 'xbox series'
            }

            platform_name = platform_mapping.get(platform_name, platform_name)
            
            if platform == platform_name:
                return release_date
    if game_info == []:
        return "No games were found matching the query."
    if len(game_info) == 100:
        return 'The query returned the maximum limit of 100 games. It is likely that the game you\'re looking for is beyond this limit.'
    return "Release date not found for specified platform."

# reads csv file, fetches release dates and writes to a text file
def create_date_list(csv_filename, filename):
    release_dates = []
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        game_count = 0
        for row in reader:
            game_count += 1
            num_columns = len(row)
        check = take_user_input('There are ' + str(game_count) + ' games, meaning this will take ' + str(game_count) + ' API calls to complete. Do you wish to continue? (y/n): ')
        print()
        if check.lower() == 'y':
            csvfile.seek(0)
            game_current = 0
            if num_columns == 1:
                for row in reader:
                    if api_calls < 360:
                        game_current += 1
                        remove_menu(1)
                        print("Game " + str(game_current) + "/" + str(game_count))
                        name = row[0]
                        data = extract_game_info(get_data(name), name)
                        release_dates.append(str(data))
            elif num_columns == 2:
                for row in reader:
                    if api_calls < 360:
                        game_current += 1
                        remove_menu(1)
                        print("Game " + str(game_current) + "/" + str(game_count))
                        name, platform = row
                        data = extract_game_info(get_data(name), name)
                        release_date = get_release_date_for_platform(data, platform)
                        release_dates.append(release_date)
                    else:
                        write_date_list(release_dates, filename)
                        pause(filename)
            else:
                print('Wrong number of columns!')
                return None
            write_date_list(release_dates, filename)
            remove_menu(1)
            print()
            print('Done. Saved to ' + filename)
            print()
            print("API Calls Made Within Hour: " + str(api_calls) + "/360")
            print()

# saves the current program configuration
def save():
    file = open("save.txt","w")
    file.write(api_key + '\n')
    file.write(str(launch_time) + '\n')
    file.write(str(api_calls) + '\n')
    file.write(str(limit) + '\n')
    file.write(str(exact_query_match) + '\n')
    file.write(str(year_only) + '\n')

# removes lines from the terminal
def remove_menu(lines):
    delete = lines
    while delete > 0:
        print ("\033[A                                                                           \033[A")
        delete -= 1

# takes user input as a string
def take_user_input(message):
    repeat = True
    while repeat == True:
        string = input(message)
        if string:
            return string.strip()
        else:
            print("Invalid Input!")

# pauses program for an hour to refresh hourly API call limit
def pause(filename):
    seconds = 3601
    while seconds > 0:
        seconds -= 1
        remove_menu(2)
        secs = seconds % (24 * 3600)
        hour = seconds // 3600
        secs0 = secs
        secs0 %= 3600
        minutes = seconds // 60
        secs1 = secs0
        secs1 %= 60
        print("Waiting for 360 more API calls, progress has been saved to " + filename + ".\nTime Remaining: " + "%d:%02d:%02d" % (hour, minutes, secs1))
        time.sleep(1)
    global api_calls
    api_calls = 0

# takes game title as input and prints results
def handle_query(game_title):
    print("Searching...")
    games_info = extract_game_info(get_data(game_title),game_title)

    if games_info != []:
        print()
        if exact_query_match == False:
            print(str(len(games_info)) + ' games match the query \'' + game_title + '\'.')
            print('Here are the release dates for each game matching \'' + game_title + '\' for the respective platforms:')
            print()
        else:
            print(str(len(games_info)) + ' games exactly match the query \'' + game_title + '\'.')
            print('Here are the release dates for each game matching \'' + game_title + '\' for the respective platforms:')
            print()
        for game in games_info:
            print(f"{html.unescape(game['title'])}")
            for platform, date in game['release_dates'].items():
                print(f"- {platform}: {date}")
            print()
        if len(games_info) == 100:
            print('The query returned the maximum limit of 100 games. If you can\'t find the game you\'re looking for, it might be beyond this limit.')
            print()
    else:
        if exact_query_match == True:
            print('No games were found that exactly match \'' + game_title + '\'.')
            print()
        else:
            print('No games were found matching \'' + game_title + '\'.')
            print()
    print("API Calls Made Within Hour: " + str(api_calls) + "/360")
    print()

# main function that acts as a menu for user interaction
def main():
    initialize()
    global api_key
    global limit
    global exact_query_match
    global year_only
    menu = True
    while menu == True:
        print("Would you like to:")
        print("1. Load CSV of Games and Create Date List")
        print("2. Enter Game Title Manually and Get Release Dates")
        print("3. Change Settings")
        print("4. Exit Program")
        choice = take_user_input("")

        if choice == "1":
            remove_menu(6)
            name = take_user_input("Enter the name of the game list CSV file: ")
            filename = take_user_input("Name the output file (remember to include the file extension, e.g., .txt, .csv): ")
            create_date_list(name, filename)
            save()

        elif choice == "2":
            remove_menu(6)
            game_title = take_user_input("Enter the title of the game (not case sensitive): ")
            handle_query(game_title)        
            save()       

        elif choice == "3":
            remove_menu(6)
            with open("save.txt","r") as file:
                lines = file.read().splitlines()
            print("1. api_key = " + str(lines[0]))
            print("2. Limit = " + str(lines[3]))
            print("3. Exact Query Match = " + str(lines[4]))
            print("4. Year Only = " + str(lines[5]))
            print("5. Go Back to Menu")
            choice = take_user_input("")
            if choice == "1":
                remove_menu(5)
                key = take_user_input("Enter new api key: ")
                api_key = key
                save()
            elif choice == "2":
                remove_menu(5)
                new_limit = take_user_input("Enter new limit (max 100): ")
                new_limit = int(new_limit)
                if new_limit > 100:
                    new_limit = 100
                limit = new_limit
                save()
            elif choice == "3":
                remove_menu(5)
                exact_match = take_user_input("Should the query require an exact match? (Enter \'t\' for True or \'f\' for False): ")
                if exact_match.lower() == 't':
                    exact_query_match = True
                else:
                    exact_query_match = False
                save()
            elif choice == "4":
                remove_menu(5)
                year = take_user_input("Would you like to get only the year, rather than the full date (year-month-day)? (Enter \'t\' for True or \'f\' for False): ")
                if year.lower() == 't':
                    year_only = True
                else:
                    year_only = False
                save()
            elif choice == "5":
                remove_menu(6)

        elif choice == "4":
            menu = False
        else:
            print("Invalid Input!")
    save()     

if __name__ == "__main__":    
    main()