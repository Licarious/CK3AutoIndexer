#ToDo List
#Adjacencies    -   Done
#Definitons     -   Done
#province map   -   Done
#default.map    -   Done
#Positions      -   Done
#...
#Things that might be useful for other people
#common\province_terrain
#common\landed_titles

import copy
import glob
from PIL import Image
import time
import math

#User Inputs
startProvicne = 0
endProvince = 10039
newStartProvicne = 0

startingDiffrence = newStartProvicne - startProvicne
newEndProvince = startingDiffrence + endProvince 

class ProvinceDefinition:
    id = 0
    red = 0
    green = 0
    blue = 0
    name = ""
    name2 = ""
    other_info = ""
    lastKnownY = -1

class Posisitions:
    id = 0
    PosX = 0.0
    PosY = 0.0
    PosZ = 0.0
    Rot1 = 0.0
    Rot2 = 0.0
    Rot3 = 0.0
    Rot4 = 0.0
    Scale1 = 0.0
    Scale2 = 0.0
    Scale3 = 0.0

class Adjacencies:
    IDfrom = 0
    IDto = 0
    adjType = ""
    IDthrough = 0
    commnet = ""
    xStart = 0
    yStart = 0
    xEnd = 0
    yEnd = 0


def get_province_deff(baseMapDefinition):
    deffMap = baseMapDefinition.read().splitlines()
    deffList = []
    x=0
    for line in deffMap:
        if "province;red;green;blue;x;x" in line:
            continue
        else:
            if x<14000:
                tmpline = line.split(';')
                try:
                    prov = ProvinceDefinition()
                    prov.red = int(tmpline[1])
                    prov.id = int(tmpline[0].lstrip("#"))
                    prov.green = int(tmpline[2])
                    prov.blue = int(tmpline[3])
                    prov.name = tmpline[4]
                    prov.other_info = tmpline[5]
                    deffList.append(prov)
                except:
                    pass
        x +=1
    return deffList

def get_adjacencies(baseMapAdjacencies):
    adjMap = baseMapAdjacencies.read().splitlines()
    adjList = []
    x=0
    for line in adjMap:
        if "From;To;Type;Through;" in line or line.startswith('-1;-1;-1;-1;'):
            continue
        else:
            tmpline = line.split(';')
            try:
                adj = Adjacencies()
                adj.IDto = int(tmpline[1])
                adj.IDfrom = int(tmpline[0])
                adj.adjType = tmpline[2]
                adj.IDthrough = int(tmpline[3])
                adj.xStart = int(tmpline[4])
                adj.yStart = int(tmpline[5])
                adj.xEnd = int(tmpline[6])
                adj.yEnd = int(tmpline[7])
                adj.commnet = tmpline[8]
                if (adj.IDfrom >= startProvicne and adj.IDfrom <= endProvince) or (adj.IDto >= startProvicne and adj.IDto <= endProvince) or (adj.IDthrough >= startProvicne and adj.IDthrough <= endProvince):
                    adjList.append(adj)
            except IndexError:
                pass
    return adjList

def get_positions(MapPositions):
    PosLines = MapPositions.read().splitlines()
    provList = []
    provId=-1
    indintation = 0
    prov = Posisitions()
    for line in PosLines:
        if indintation == 3:
            if line.strip().startswith("id="):
                provId=int(line.strip().split("=")[1])
                if provId >= startProvicne and provId <= endProvince:
                    prov = Posisitions()
                    prov.id =provId
            if line.strip().startswith("position="):
                if provId >= startProvicne and provId <= endProvince:
                    prov.PosX = float(line.strip().split(" ")[1])
                    prov.PosY = float(line.strip().split(" ")[2])
                    prov.PosZ = float(line.strip().split(" ")[3])
            if line.strip().startswith("rotation="):
                if provId >= startProvicne and provId <= endProvince:
                    prov.Rot1 = float(line.strip().split(" ")[1])
                    prov.Rot2 = float(line.strip().split(" ")[2])
                    prov.Rot3 = float(line.strip().split(" ")[3])
                    prov.Rot4 = float(line.strip().split(" ")[4])
            if line.strip().startswith("scale="):
                if provId >= startProvicne and provId <= endProvince:
                    prov.Scale1 = float(line.strip().split(" ")[1])
                    prov.Scale2 = float(line.strip().split(" ")[2])
                    prov.Scale3 = float(line.strip().split(" ")[3])

        if "{" in line or "}" in line:
            #print("l: "+line)
            for element in list(line.strip()):
                if "{" in element:
                    indintation +=1
                    #print("s: "+element)
                elif "}" in element:
                    indintation -=1
                    if indintation == 2:
                        if provId>-1:
                            provList.append(prov)
                            provId=-1
                    #print("e: "+element)
                elif "#" in element:
                    #print("c: "+element)
                    break
    return provList

def getRiverList(defaultMap):
    tmpList = []
    for line in defaultMap:
        if line.strip().startswith("#"):
            pass
        elif line.strip().startswith("river_provinces"):
            if "RANGE" in line:
                x1=0
                x2=0
                #print(line)
                words = line.split(" ")
                for word in words:
                    if "#" in word:
                        break
                    else:
                        try:
                            if x1 == 0:
                                x1 = int(word)
                            elif x2 == 0:
                                x2 = int(word)
                        except:
                            pass
                for i in range(x1,x2+1):
                    tmpList.append(i)
                #print("%s,%s"%(x1,x2))
            elif "LIST" in line:
                words = line.split(" ")
                for word in words:
                    if "#" in word:
                        break
                    else:
                        try:
                            tmpList.append(int(word))
                        except:
                            pass
    return tmpList

def write_DefaultMap(INRDefaultMap):
    defaultMapList = []
    defaultMap = INRDefaultMap.read().splitlines()
    skipCount = 10
    for line in defaultMap:
        for i in range(startProvicne,endProvince+1):
            if str(i) in line or line.strip().startswith("#MNR"):
                skipCount = 0
            else:
                skipCount+=1
            if str(i) in line or line.strip().startswith("#MNR") or skipCount < 3 or line.strip() == "":
                if line not in defaultMapList:
                    defaultMapList.append(line)
                    break
            

    DefaultMap = open("Output\\map_data\\defalut_Output.map", "w",encoding='utf-8',errors='ignore')
    for line in defaultMapList:
        tmpLine = line.split(" ")
        for index in tmpLine:
            try:
                id = int(index)
                if id >= startProvicne and id <= endProvince:
                    id += startingDiffrence
                DefaultMap.write("%i "%id)
            except:
                DefaultMap.write("%s "%index)
        DefaultMap.write("\n")
    DefaultMap.close()

def write_Positions(tmpNewPos,file):
    tmpFileString = "Output\\" + file.lstrip("ModInput\\").rstrip(".txt")+"_output.txt"
    #print(tmpFileString)
    Positions = open(tmpFileString, "w",encoding='utf-8',errors='ignore')
    for prov in tmpNewPos:
        #print(prov.id)
        Positions.write("\n\t\t{")
        Positions.write("\n\t\t\tid=%g"%prov.id)
        Positions.write("\n\t\t\tposition={ %f %f %f }"%(prov.PosX,prov.PosY,prov.PosZ))
        Positions.write("\n\t\t\trotation={ %f %f %f %f }"%(prov.Rot1,prov.Rot2,prov.Rot3,prov.Rot4))
        if prov.id in riverList:
            Positions.write("\n\t\t\tscale={ 0.5 0.5 0.5 }")
        else:
            Positions.write("\n\t\t\tscale={ %f %f %f }"%(prov.Scale1,prov.Scale2,prov.Scale3))
        Positions.write("\n\t\t}")
    Positions.close()

def write_Definitions(deffList,newStartProvicne,newEndProvince):
    outputDeff = open("Output\\map_data\\definitions_Output.csv", "w",encoding='utf-8',errors='ignore')
    for prov in deffList:
        
        if prov.id >= newStartProvicne and prov.id <= newEndProvince:
            #print(prov.name)
            outputDeff.write("\n%g;"%prov.id)
            outputDeff.write("%g;"%prov.red)
            outputDeff.write("%g;"%prov.green)
            outputDeff.write("%g;"%prov.blue)
            outputDeff.write("%s;"%prov.name)
            
            outputDeff.write("%s;"%prov.other_info)
    outputDeff.close()

def write_Adjacencies(adjList,newStartProvicne,newEndProvince):
    outputAdj = open("Output\\map_data\\adjacencies_OutPut.csv", "w",encoding='utf-8',errors='ignore')
    for prov in adjList:
        if (prov.IDfrom >= newStartProvicne and prov.IDfrom <= newEndProvince) or (prov.IDto >= newStartProvicne and prov.IDto <= newEndProvince) or (prov.IDthrough >= newStartProvicne and prov.IDthrough <= newEndProvince):
            outputAdj.write("\n")
            outputAdj.write("%g;"%prov.IDfrom)
            outputAdj.write("%g;"%prov.IDto)
            outputAdj.write("%s;"%prov.adjType)
            outputAdj.write("%g;"%prov.IDthrough)
            outputAdj.write("%g;%g;%g;%g;"%(prov.xStart,prov.yStart,prov.xEnd,prov.yEnd))
            outputAdj.write("%s"%prov.commnet)


    outputAdj.close()

def draw_UpdatedProvinces(MNRMapProvinces, smallCountyListNames, newSmallCountyListNames):
    pixMNR = MNRMapProvinces.load()
    img = Image.new(MNRMapProvinces.mode, MNRMapProvinces.size, 'white')
    pixNew = img.load()
    x1,y1=0,0
    x2,y2=MNRMapProvinces.size[0],MNRMapProvinces.size[1]
    counter = math.ceil((y2-y1)/50)
    #print(len(smallCountyListNames))
    tupleList = []
    newTupleList = []
    lastY = []
    for prov in smallCountyListNames:
        tupleList.append((prov.red,prov.green,prov.blue,255))
        lastY.append(-1)
    for prov in newSmallCountyListNames:
        newTupleList.append((prov.red,prov.green,prov.blue,255))

    tmpTotal = len(tupleList)
    count = 0
    #print(tupleList)
    #print(counter)
    for y in range(y1,y2):
        if y%counter == 0:
            #print("%i%%"%((y*5)/counter))
            for i, prov in enumerate(lastY):
                if prov>-1 and prov<y-(MNRMapProvinces.size[1]/40):
                    #print(tupleList[i])
                    del lastY[i]
                    del tupleList[i]
                    del newTupleList[i]
                    i-=1
                    count+=1
            if (count*1000/tmpTotal)/10 > (y*2)/counter:
                print("%i%%"%((count*1000/tmpTotal)/10))
            else:
                print("%i%%"%((y*2)/counter))
        for x in range(x1,x2):
            if pixMNR[x,y] in tupleList:
                #print(tupleList.index(pixMNR[x,y]))
                pixNew[x,y] = copy.deepcopy(newTupleList[tupleList.index(pixMNR[x,y])])
                lastY[tupleList.index(pixMNR[x,y])] = y
            pass
    img.show()
    img.save("Output\\map_data\\province_Output.png")
    img.close()


ts = time.time()

modInputDefinition = open("modInput\\map_data\\definition.csv")
modInputAdjacencies = open("modInput\\map_data\\adjacencies.csv")
modInputProvinces = Image.open("modInput\\map_data\\provinces.png")
INRDefaultMap = open("ModInput\\map_data\\default.map")

adjList = get_adjacencies(modInputAdjacencies)
deffList = get_province_deff(modInputDefinition)

#Get list of all rivers
riverList = getRiverList(INRDefaultMap)

#Grab all provinces that will be effected by change
smallCountyListNames = []
for prov in deffList:
    #print("%s, %s"%(county.id,startProvicne))
    if prov.id >= startProvicne and prov.id <= endProvince:
        smallCountyListNames.append(copy.deepcopy(prov))
        #print(county.name)
    pass

#Set province name in new spot
newSmallCountyListNames = []
i=0
for prov in deffList:
    if prov.id >= newStartProvicne and prov.id <= newEndProvince:
        #print("%g, %g, %s"%(i,county.id,county.name))
        #print((smallCountyListNames[i]).name  )
        prov.name = (smallCountyListNames[i]).name  
            
        prov.other_info = (smallCountyListNames[i]).other_info
        newSmallCountyListNames.append(copy.deepcopy(prov))
        i +=1
    pass


#get and update lines containing province ID in adjancies.csv
for prov in adjList:
    if prov.IDfrom >= startProvicne and prov.IDfrom <= endProvince:
        prov.IDfrom += startingDiffrence
    if prov.IDto >= startProvicne and prov.IDto <= endProvince:
        prov.IDto += startingDiffrence
    if prov.IDthrough >= startProvicne and prov.IDthrough <= endProvince:
        prov.IDthrough += startingDiffrence
    pass

#get all river provinces positions that will be effected by change
PositionFiles = glob.glob('ModInput/gfx/map/map_object_data/*_locators.txt')
for file in PositionFiles:
   tmpPos = get_positions(open(file))
   tmpNewPos = []
   for prov in tmpPos:
       if int(prov.id) >= startProvicne and int(prov.id) <= endProvince:
           prov.id = int(prov.id) + startingDiffrence
           tmpNewPos.append(prov)
   write_Positions(tmpNewPos,file)

write_Definitions(newSmallCountyListNames,newStartProvicne,newEndProvince)
write_Adjacencies(adjList,newStartProvicne,newEndProvince)
write_DefaultMap(INRDefaultMap)
draw_UpdatedProvinces(modInputProvinces, smallCountyListNames, newSmallCountyListNames)


ts2 = time.time()
print("%g Seconds"%(ts2 - ts))