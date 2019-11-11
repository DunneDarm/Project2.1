def currentLight(serialread):
    byteList= []
    value= ""
    while(1) :
        bytes= serialread.decode('utf-8')
        if bytes != 'L':
            byteList.append(bytes)
        elif bytes == 'L':
            break

    for i in byteList:
        value += i

    return value

def LightLineData(serialread):
    LumenList = []
    bytes = serialread.decode('utf-8')
    bytes = bytes.split("L")
    bytes = bytes[1:21]
    for light in bytes:
        LumenList.append(int(light))
    return LumenList