import json


def put_data(speed, time):
    with open('data.json','r') as f :
            
        data = json.load(f)
        (data["speed"].append(speed))
        (data["time"].append(time))
        # f.write(json.dumps(data))
        x = json.dumps(data)
    with open('data.json','w') as f:
        f.write(x)

put_data(1,1)