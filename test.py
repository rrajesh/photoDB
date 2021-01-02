import json
import os
import sys
import exifread
import logging

def printExifInfo(entryList,filePath):
    logging.info("processing file: " + filePath)
    f = open(filePath,"rb")
    f_entry = {}
    f_entry['fileName'] = os.path.basename(filePath)

    try:
        tags = exifread.process_file(f)
    except UnicodeDecodeError:
        logging.error("error during processing " + filePath)
        f.close()
        entryList[filePath] = f_entry
        return
    except struct.error:
        logging.error("error during processing " + filePath)
        f.close()
        entryList[filePath] = f_entry
        return
    except:
        logging.error("error during processing " + filePath)
        f.close()
        entryList[filePath] = f_entry
        return

    for tag in tags.keys():
        if tag[:4]=='Imag' or tag[:4]=="EXIF":
            #print('key: {}, value: {}'.format(tag,tags[tag]))
            logging.info("key: " + tag + ", value: " + str(tags[tag]))
            f_entry[tag] = str(tags[tag])
    f.close()
    entryList[filePath] = f_entry


def printUsage():
        print("INSUFFICIENT ARGUMENTS\n")
if __name__ == "__main__":
    numArgs = len(sys.argv)
    scriptName = sys.argv[0]
    dir = sys.argv[1]
    myEntries = {}
    myDirs = {}
    logging.basicConfig(filename="photoProcessing.log", filemode="w",format='%(levelname)s - %(message)s',level=logging.DEBUG)
    # list comprehension
    jFile = open(r'c:\users\rip\Desktop\picInfo.json',"r")
    myEntries = json.load(jFile)
    myDirs = myEntries['directories']
    jFile.close()
    LL=[(r,d,f) for r,d,f in os.walk(dir)]
    for entry in LL:
        root = entry[0]
        cdirs = entry[1]
        cfiles = entry[2]
        try:
            if root in myDirs:
                #print("directory {} already processed".format(root))
                logging.info("directory: " + root + " already processed")
                continue
            else: 
                myDirs[root] = 1
            for fname in cfiles:
                fpath = os.path.join(root,fname)
                logging.info("file: " + fpath)
                if (fpath[-3:].upper() == "JPG"):
                    printExifInfo(myEntries,fpath)
        except:
            print("ignore error")
    myEntries['directories'] = myDirs
    # json string
    yy = json.dumps(myEntries)
    #jFile.write(myEntries)
    #print(str(myEntries))
    jFile = open(r'c:\users\rip\Desktop\picInfo.json',"w")
    json.dump(myEntries,jFile,skipkeys=True,indent=4)
    jFile.close()
    
    #json.dump(myEntries,jFile,indent=4)
    
    #jFile.close()
