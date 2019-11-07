def currenttemp(serialread):
    return str(serialread)[2:-1]

def TempLineData(serialread):
    tempString = str(serialread)[2:-1]
    if tempString[-1] == "t":
        tempString = tempString[:-1]
    templist = tempString.split("t")
    templist = list(map(int, templist))

    return templist
