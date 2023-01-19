def get_score(speedValAsList, timeArray, old_score):
    print(speedValAsList, timeArray, old_score)
    accelAsList = [speedValAsList[x] - speedValAsList[x-1]
                   for x in range(1, len(speedValAsList))]
    log = []
    breakScore, accelScore = 0, 0
    for z in range(len(speedValAsList) - 1):
        # it will start from zero to 1, this means as time increase
        timeSeries = timeArray[z]/(1+timeArray[z])
        # print(z)
        x = accelAsList[z]/(timeArray[z]-timeArray[z-1])
        if (7 <= abs(x)):
            if (x > 0):
                accelScore += 5*timeSeries
                log.append(f"accelerates {round(x , 2)}, {timeArray[z]}")
            elif x <= -8:
                breakScore += 10*timeSeries
                log.append(f"decelerates {round(x , 2)}, {timeArray[z]}")
        elif (6 <= abs(x)):
            if (x > 0):
                accelScore += 2.5*timeSeries
                log.append(f"accelerates {round(x , 2)}, {timeArray[z]}")
            elif x <= -7:
                breakScore += 5*timeSeries
                log.append(f"decelerates {round(x , 2)}, {timeArray[z]}")

    c = 100 - breakScore - accelScore
    score = 0 if c < 0 else c

    # 0.5 is the factor of change, both factor must be = 1
    c = 0.5 * (old_score + score)
    weightedScore = 0 if c < 0 else c

    # {"score" : score}

    print(log, len(log))
    return {"score": score, "weightedScore": weightedScore, "breakScore": breakScore, "accelScore": accelScore, 'Max Speed': max(speedValAsList)}
    # print(" Your score is %d out of 100,\n Your total score is %d out 100 \n With max speed : %.2f km/h and max accleartion: %.2f km/h^2" %
    #       (score, weightedScore, max(speedValAsList), max(accelAsList)))
