# global dictionaries to keep track of imported data

baselightData = {
    "files": [],
    "shots" :[]
}

XytechData = {}

#method that processes the intial baselight export text file
def processBL():
    # open reading connection to file
    with open("Baselight_export.txt", "r") as bl_file:
        baselight = bl_file.readline()
        #parse file until no more data
        while baselight != "":
            #check in case empty lines in file to avoid processing errors
            if baselight.rstrip("\n") == "":
                baselight = bl_file.readline()
                continue
            #split each line, remove file location, create shot list, and then store it in dictionary
            bl = baselight.rstrip("\n").split("Dune2")
            bl = remove_filePath(bl)
            key, shots = parseShots(bl)
            baselightData["files"].append(key)
            baselightData["shots"].append(shots)
            baselight = bl_file.readline()
            # loop to read data until eof
    #close file connection
    bl_file.close()
               
#method that processes xytech text file
def process_Xytech():
    #open file for reading
    with open("Xytech.txt", 'r') as xytech_file:
        xy = xytech_file.readline()
        # loop until end of file
        while xy != "":
            #because there are empty lines before eof, check to avoid processing errors
            if xy.rstrip("\n") == "":
                xy = xytech_file.readline()
                continue
            #checking for individual fields to store for later export
            if "Producer" in xy:
                xy = xy.rstrip("\n").split(":")
                XytechData["Producer"] = xy[1].rstrip("\n").strip()
            if "Operator" in xy:
                xy = xy.rstrip("\n").split(":")
                XytechData["Operator"] = xy[1].rstrip("\n").strip()
            if "Job" in xy:
                xy = xy.rstrip("\n").split(":")
                XytechData["Job"] = xy[1].rstrip("\n").strip()

            # create
            if "Dune2" in xy:
                xy = xy.rstrip("\n").split("Dune2")
                # check if xytech file locations exist
                if check_Xytech(xy[0]) == True:
                    #if location exists, append new scene
                    XytechData[str(xy[0])].append(xy[1])
                else:
                    # if doesn't exist, create new scene list for location
                    XytechData[str(xy[0])] = [str(xy[1])]

            if "Notes" in xy:
                xy = xy.rstrip("\n")
                XytechData["Notes"] = xytech_file.readline().rstrip("\n")
            xy = xytech_file.readline()
        #close file connection
        xytech_file.close()

#method that specifically removes the split file path
def remove_filePath(line):
    line = list(line)
    return line[1].split(" ")

# method that ceates a shotlist for specified file location
def parseShots(line):
    line = list(line)
    key = line[0]
    shots = []
    for i in range(1, len(line)):
        if str(line[i]).isnumeric():
            shots.append(line[i])
    return key, shots

#check if file location exists in Xytech data
def check_Xytech(line):
    if line in XytechData.keys():
        return True
    return False

# method that exports all data
def export():
    #open file for writing data
    with open("export.csv", 'w') as export:
        #writes meta data about producer, operator, job, and notes
        export.write("Proucer,Operator,Job,Notes\n")
        export.write(XytechData["Producer"] + "," + XytechData["Operator"] + "," + XytechData["Job"] +"," + XytechData["Notes"] + "\n\n")
        export.write("Show Location,Frames to Fix\n")
        shotListIndex = 0
        #loop through all file locations in baselight and grab new file location from Xytech
        for key in baselightData["files"]:
            shotList = baselightData["shots"][shotListIndex]
            newFile = str(get_fileLocation(key))
            export.write(newFile + key +", " + shotList[0])
            #loop through the shotlists for each files location
            counter = 1
            for i in range(1, len(shotList)):
                if int(shotList[i]) > int(shotList[i-1]) + 1:
                    if counter == 1:
                        export.write("\n" + newFile+ key +", " + shotList[i])
                    else:
                        export.write("-" + shotList[i-1] + "\n" + newFile+ key +", " + shotList[i])
                        counter = 1
                else:
                    counter += 1
            if counter > 1:
                export.write("-" + shotList[i])
            export.write("\n")
            shotListIndex+=1
    export.close()

def get_fileLocation(key):
    for newLocation in XytechData.keys():
        for file in XytechData[newLocation]:
            if key == file:
                return newLocation + "Dune2"
           
# main method calling subsequent methods
def main():
    processBL()
    process_Xytech()
    export()

main()
