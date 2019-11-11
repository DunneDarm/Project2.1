def currentLight(serialread):
    byteList= []
    value= ""
    while(1) :
        bytes= serialread().decode('utf-8')
        if bytes != 'L':
            byteList.append(bytes)
        elif bytes == 'L':
            break

    for i in byteList:
        value += i

    return value

def LightLineData(serialread) :
    lightvalues = []
    listholder = []
    strholder = ""

    while (1):
        bytes = serialread().decode('utf-8')

        if bytes != 'L':
            listholder.append(bytes)
        elif bytes == 'L':
            for i in listholder:
                strholder += i
            lightvalues.append(strholder)
            listholder = []
            strholder = ""
    return lightvalues