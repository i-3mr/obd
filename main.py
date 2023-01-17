import obd
from time import sleep
from get_score import get_score
import requests
from requests.auth import HTTPBasicAuth
import datetime
import time
from file import put_data
import json

ID = "6003277"

token = HTTPBasicAuth("s202159910@kfupm.edu.sa", "OmAr11223")


def post(d):
    res = requests.post(
        "https://env573108.us.cumulocity.com/measurement/measurements", json=d, auth=token)
    if res.status_code == 201:
        print("SENT : ", d["type"])
    else:
        print("FAILED ", res.status_code)


def postAll(obj):
    for i in obj:
        post({
            f"c8y_{i}": {
                "S": {
                    "value": obj[i],
                    "unit": ""
                }
            },
            "time": datetime.datetime.utcfromtimestamp(time.time()).isoformat()+"Z",
            "source": {
                "id": ID},
            "type": i
        })


old_score = 0

with open('data.json', 'r') as f:
    data = json.load(f)
    if len(data["speed"]) > 0:
        old_score = data["score"]  # get_old_score()
        score = get_score(data["speed"], data["time"], old_score)
        postAll(score)
        f.close()
        with open('data.json', 'w') as f:
            f.write('{"speed":[],"time":[],"score":'+str(score["score"])+"}")
    else:
        print("not data")


while not obd.OBD("/dev/cu.usbserial-10", baudrate=38400).is_connected():
    sleep(1)

connect = obd.OBD("/dev/cu.usbserial-10", baudrate=38400)

print('connection :', connect.is_connected())

time_start = time.time()
counter = 0
while connect.is_connected():
    old_speed = 0
    for i in ["SPEED", "RPM", "RUN_TIME", "DISTANCE_W_MIL", "FUEL_PRESSURE", "FUEL_RATE"]:

        cmd = obd.commands[i]
        res = connect.query(cmd)
        fragment = (str(cmd).split(":")[1].strip())
        value = res.value.magnitude
        time_ = datetime.datetime.utcfromtimestamp(time.time()).isoformat()+"Z"
        unit = str(res.unit)
        # print(cmd)
        sId = ID  # change

        if i == "SPEED":
            old_speed = value
            put_data(value, time.time() - time_start)

        post({
            f"c8y_{fragment}": {
                "S": {
                    "value": value,
                    "unit": unit
                }
            },
            "time": time_,
            "source": {
                "id": sId
            },
            "type": fragment
        })

# with open("xxxuy.txt", 'w') as file:
#     # get the old score in cumulocity
#     file.write(get_score(speedList, timeList, 0))
#     file.write('\n')




# file = open('dh7.csv', 'w')
# for i in obd.commands[1]:
#     string = str(i)+','
#     file.write(string)
# file.write(r'\n')
# for i in list3:
#     for j in i:
#         house = str(i)+','
#         file.write(house)
#     file.write(r'\n')

# file.close()
