import requests
import time
import re

with open("titles.txt") as x:
    titles = x.read().splitlines()
with open("id_list.txt") as y:
    ids = y.read().splitlines()

id_list = []
date_list = []
api_key = "moby_YXyzhJMmxrbwCTmUy5TfnLUfQu5"

##########

def get_id(title):
    url = "https://api.mobygames.com/v1/games"
    params = {"api_key":api_key,"title":title,"format":"id","limit":"1"}

    response = requests.get(url, params)

    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(response.status_code)

def get_date(id):
    url = "https://api.mobygames.com/v1/games/" + str(id) + "/platforms"
    params = {"api_key":api_key}

    response = requests.get(url, params)

    if response.status_code == 200:
        data = response.json()
        return(data)
    else:
        print(response.status_code)

##########

def extract_id(data):
    for key, value in data.items():
        value = str(value)
        value = value[1:]
        value = value[:-1]
        value = int(value)
        return(value)

def extract_date(data):
    data = str(data)
    date = re.findall(r'\d+', data)
    return date
print(extract_date(get_date(623)))
##########

def make_id_list(value):
    id_list.append(value)
    print(id_list)

def make_date_list(value):
    date_list.append(value)
    print(date_list)

##########

def write_id_list():
    file = open("id_list.txt","w")
    for i in id_list:
        file.write(str(i)+"\n")
    file.close()

def write_date_list():
    file = open("date_list.txt","w")
    for d in date_list:
        file.write(str(d)+"\n")
    file.close()

##########

def create_id_list():
    for t in titles:
        make_id_list(extract_id(get_id(t)))
        time.sleep(1)
    
    write_id_list()

def create_date_list():
    for i in ids:
        make_date_list(extract_date(get_date(i)))
        time.sleep(1)
    
    write_date_list()

#create_date_list()

## good human to computer interaction

## robust exception handling