import json

def getData():
    file = open('data.json', 'r')
    data = json.load(file)
    return data

def setData(data):
    file = open('data.json', 'w')
    json.dump(data, file)
