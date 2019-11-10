def currenttemp(serialread):
    return str(serialread)[2:-1]

def TempLineData(serialread):
    Realtemplist = []
    tempString = str(serialread)[2:-1]
    if tempString[-1] == "t":
        tempString = tempString[:-1]
    templist = tempString.split("t")

    for temp in templist:
        Realtemplist.append(int(temp))

    return Realtemplist
