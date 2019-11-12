def TempLineData(serialread):
    Realtemplist = []
    tempString = str(serialread)[2:-1]
    if tempString[-1] == "t":
        tempString = tempString[:-1]
    templist = tempString.split("t")
    templist = templist[1:21]

    for temp in templist:
        Realtemplist.append(int(temp))

    return Realtemplist

def TempData(serialread):
    bytes = serialread.decode('utf-8')
    bytes = bytes.split("t")
    bytes = int(bytes[1])
    return bytes
