import json
import os
import sys
import datetime
import sqlite3
import logging
def printExifInfo(entryList,filePath):
    f = open(filePath,"rb")
    tags = exifread.process_file(f)
    f_entry = {}
    f_entry['fileName'] = os.path.basename(filePath)
    for tag in tags.keys():
        if tag[:4]=='Imag' or tag[:4]=="EXIF":
            #print('key: {}, value: {}'.format(tag,tags[tag]))
            f_entry[tag] = str(tags[tag])
    f.close()
    entryList[filePath] = f_entry


def printUsage():
        print("INSUFFICIENT ARGUMENTS\n")
if __name__ == "__main__":
    numArgs = len(sys.argv)
    #scriptName = sys.argv[0]
    #dir = sys.argv[1]   
    jFile = open(r'c:\users\rip\Desktop\picInfo2.json',"r")
    logging.basicConfig(filename="photoProcessing.log", filemode="w",format='%(levelname)s - %(message)s',level=logging.DEBUG)
    myEntries = json.load(jFile)
    conn = sqlite3.connect(r'c:\users\rip\Desktop\testDB.sqlite')
    c = conn.cursor()
    create_table_q = ''' create table if not exists photos
                      (id integer primary key not null,
                       "Image Make" text,
                       "Image Model" text,
                       "EXIF ExposureTime" text,
                       "EXIF FNumber" text,
                       "EXIF DateTimeOriginal" timestamp,
                       "DateTime" text,
                       "EXIF LensMake" text,
                       "EXIF LensModel" text,
                       "EXIF ExposureProgram" text,
                       "EXIF ISOSpeedRatings" text,
                       path text)'''
    c.execute(create_table_q)
    create_entry_q = '''insert into  photos (
                id,
                "Image Make",
                "Image Model",
                "EXIF ExposureTime",
                "EXIF FNumber",
                "EXIF DateTimeOriginal",
                "DateTime",
                "EXIF LensMake",
                "EXIF LensModel",
                "EXIF ExposureProgram",
                "EXIF ISOSpeedRatings",
                path)
                values(?,?,?,?,?,?,?,?,?,?,?,?)'''
    id = 0
    for key,value in myEntries.items():
        print(key)
        print(value)
        print(id)
        myTuple = []
        myTuple.append(id)
        id = id + 1
        fid = 0
        print(value.keys())
        if "Image Make" in value:
            myTuple.append(value["Image Make"])
            fid = fid + 1
        else:
            myTuple.append("")
        if "Image Model" in value:
            myTuple.append(value["Image Model"])
            fid = fid + 1
        else:
            myTuple.append("")
        if "EXIF ExposureTime" in value:
            myTuple.append(value["EXIF ExposureTime"])
            fid = fid + 1
        else:
            myTuple.append("")
        if "EXIF FNumber" in value:
            myTuple.append(value["EXIF FNumber"])
        else:
            myTuple.append("")
        if "EXIF DateTimeOriginal" in value:
            dt_str = value["EXIF DateTimeOriginal"]
            datetime_obj = datetime.datetime.strptime(dt_str,"%Y:%m:%d %H:%M:%S")
            timestamp = datetime_obj.timestamp()
            myTuple.append(timestamp)
            myTuple.append(dt_str)
            fid = fid + 1
        else:
            myTuple.append("")
        if "EXIF LensMake" in value:
            myTuple.append(value["EXIF LensMake"])
            fid = fid + 1
        else:
            myTuple.append("")
        if "EXIF LensModel" in value:
            myTuple.append(value["EXIF LensModel"])
        else:
            myTuple.append("")
        if "EXIF ExposureProgram" in value:
            myTuple.append(value["EXIF ExposureProgram"])
            fid = fid + 1
        else:
            myTuple.append("")
        if "EXIF ISOSpeedRatings" in value:
            myTuple.append(value["EXIF ISOSpeedRatings"])
        else:
            myTuple.append("")
        myTuple.append(key)#path
        print(str(myTuple))
        if fid < 5:
            id = id - 1
            continue
        c.execute(create_entry_q,tuple(myTuple))
    conn.commit()
    jFile.close()
    
