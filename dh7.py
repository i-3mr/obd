

def score(speed, oldSpeed, maxMin):
    # inital value for score levels
    overSpeedLevel5count = 0
    overSpeedLevel4count = 0
    overSpeedLevel3count = 0
    overSpeedLevel2count = 0
    overSpeedLevel1count = 0
    # accel
    accelLevel5count = 0
    accelLevel4count = 0
    accelLevel3count = 0
    accelLevel2count = 0
    accelLevel1count = 0
    # break
    breakLevel5count = 0
    breakLevel4count = 0
    breakLevel3count = 0
    breakLevel2count = 0
    breakLevel1count = 0

    x = speed
    z = speed - oldSpeed

    if(speed > maxMin["currentMax"]):
        maxMin["currentMax"] = speed
    if(speed < maxMin["currentMin"]):
        maxMin["currentMin"] = speed

    if (x >= 220):  # the value 220 should be the speed of the road not a fixed number, if we have time we should do it
        overSpeedLevel5count += 1
    elif (x >= 200):
        overSpeedLevel4count += 1
    elif (x >= 180):
        overSpeedLevel3count += 1
    elif (x >= 160):
        overSpeedLevel2count += 1
    elif (x >= 145):
        overSpeedLevel1count += 1
    # Calc Accel
    if (7 <= abs(z)):
        if (z > 0):
            accelLevel5count += 1
        else:
            breakLevel5count += 1
    elif (6 <= abs(z)):
        if (z > 0):
            accelLevel4count += 1
        else:
            breakLevel4count += 1
    elif (5 <= abs(z)):
        if (z > 0):
            accelLevel3count += 1
        else:
            breakLevel3count += 1
    elif (4 <= abs(z)):
        if (z > 0):
            accelLevel2count += 1
        else:
            breakLevel2count += 1
    elif (3 <= abs(z)):
        if (z > 0):
            accelLevel1count += 1
        else:
            breakLevel1count += 1

    weightedScore = 0

    overSpeedScore = (overSpeedLevel5count*30)+(overSpeedLevel4count*20) + \
        (overSpeedLevel3count*10)+(overSpeedLevel2count*5)+(overSpeedLevel1count*1)

    breakscore = (breakLevel5count*1)+(breakLevel4count*1) + \
        (breakLevel3count*1)+(breakLevel2count*1)+(breakLevel1count*1)

    accelscore = (accelLevel5count*10)+(accelLevel4count*5) + \
        (accelLevel3count*2.5)+(accelLevel2count*1.25)+(accelLevel1count*1)

    score = 100 - breakscore - accelscore - overSpeedScore

    if score < 0:
        score = 0
    # 0.5 is the factor of change, both factor must be = 1
    weightedScore = 0.7*weightedScore + 0.3*score
    print(f"breakLevel5count : {breakLevel5count}")
    print("Your score is %d out of 100, With max speed : %.2f km/h and max accleartion: %.2f m/s^2" %
          (abs(score), maxMin["currentMax"], maxMin["currentMin"]))
    # return score
    return {"currentMax": maxMin["currentMax"], "currentMin": maxMin["currentMin"], "score": score}
