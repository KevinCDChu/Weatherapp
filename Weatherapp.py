import requests, json, pickle,os

location = input("Input location (auto for Waterloo): ")
appid = "921690e0595dab330f514b9b4b420884"
autoid = "6176823"

if location == "auto":
    url = "https://api.openweathermap.org/data/2.5/forecast?id=%s&appid=%s" % (autoid, appid)
else:
    url = "https://api.openweathermap.org/data/2.5/forecast?q=%s&appid=%s" % (location, appid)

response = requests.get(url)
response.raise_for_status()

jsondata = json.loads(response.text)
weatherdata = jsondata["list"]
info = {}


def save_dict():
    with open("b.txt", "wb") as b:
        pickle.dump(info, b)


def load_dict():
    if os.path.isfile(os.getcwd() + "\\b.txt"):
        with open("b.txt", "rb") as b:
            return pickle.load(b)
    else:
        return {}


def addinfo():
    with open(jsondata["city"]["name"] + ", " + jsondata["city"]["country"] + ".txt", "w") as account:
        for key in sorted(info.keys()):
            account.write("Time: " + key + "\n")
            account.write("Temperature: " + info[key][0] + "\n")
            account.write("Status: " + info[key][1] + "\n")
            account.write("\n")


def printinfo():
    for key in sorted(info.keys()):
        print("Time: " + key + "\n")
        print("Temperature: " + info[key][0] + "\n")
        print("Status: " + info[key][1] + "\n")
        print("\n")


print("Showing and downloading weather data for " + jsondata["city"]["name"] + ", " + jsondata["city"]["country"])
info = load_dict()
for i in range(len(weatherdata)):
    info[weatherdata[i]["dt_txt"]] = \
        [str(round(weatherdata[i]["main"]["temp"] - 273.15)) + " Degrees Celsius",
         weatherdata[i]['weather'][0]['main'] + ' - ' + weatherdata[i]['weather'][0]['description']]
printinfo()
addinfo()
save_dict()

