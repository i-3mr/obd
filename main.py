import obd
from time import sleep
import requests
from requests.auth import HTTPBasicAuth
import datetime
import time
from dh7 import score

maxMin = {
    "currentMin": 0,
    "currentMax": 0
}

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
                    "unit": 'm/s'
                }
            },
            "time": datetime.datetime.utcfromtimestamp(time.time()).isoformat()+"Z",
            "source": {
                "id": "6003277"
            },
            "type": i
        })


print('start')
while True:
    connect = obd.OBD("/dev/cu.usbserial-10", baudrate=38400)
    if connect.is_connected():
        break

print('connection :', connect.is_connected())

list3 = []
counter = 0
while connect.is_connected():
    old_speed = 0
    list2 = []
    for i in ["SPEED", "RPM", "RUN_TIME", "DISTANCE_W_MIL", "FUEL_PRESSURE", "FUEL_RATE"]:

        cmd = obd.commands[i]
        res = connect.query(cmd)
        fragment = (str(cmd).split(":")[1].strip())
        value = res.value.magnitude
        time_ = datetime.datetime.utcfromtimestamp(time.time()).isoformat()+"Z"
        unit = str(res.unit)
        # print(cmd)
        sId = "6003277"

        if i == "SPEED":
            a = score(value, old_speed, maxMin)
            old_speed = value
            postAll(a)
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
        list2.append(str(res.value))

    list3.append(list2)

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
