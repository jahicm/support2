import os
import shutil
import glob


def list_source_folder(reconmaps, valuepaths):
    for key in reconmaps:
        print("*************************Checking " + valuepaths + reconmaps[key] + "***********************************")
        for filename in os.listdir(valuepaths+reconmaps[key]):
            print(filename)


def list_destination_folder(reconmaps, keypaths):
    del reconmaps["Inbox.reconlsc_"]
   
    del reconmaps["Inbox.reconpay_"]
	
    for key in reconmaps:
        print("**************************Checking " + keypaths + key + "*************************************")
        for filename in os.listdir(keypaths+key):
            print(filename)


def listdirectory(keypaths, path):
    for filename in os.listdir(path):
        if filename.endswith('_'):
            print(filename+" move to "+keypaths)
            shutil.move(path+"/"+filename,keypaths+"/"+filename[:-1])
			
        elif filename.endswith('__'):
            print(filename+" move to "+keypaths)
            shutil.move(path+"/"+filename,keypaths+"/"+filename[:-2])

    print("**************************Checking " + path + "*************************************")


def reconsrename(reconmaps, valuepaths, keypaths):

    for key in reconmaps:
        destination = reconmaps[key]
        if key.endswith('_'):
            key = key[:-1]
        listdirectory(keypaths+key, valuepaths+destination)


def delete():

    keypathfull = '/cs/mqsi/data/Inbox.reconpay/'
    pattern = "0011C*"
    filelist = glob.glob(keypathfull+pattern)
    print "Default keypaths of deletion is :", keypathfull
    print "Default patter of file to delete is :", pattern

    print "Delete y/n ?"
    answer = raw_input()

    if answer == "y":
        for filePath in filelist:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)
            print "DELETED ", filePath


def process_message_dropped(keypaths,path,valuepath,reconmaps):

    reconlsc="Inbox.reconlsc"
    reconpay="Inbox.reconpay"
    reconfor="Inbox.reconpay_"

    print "Please provide name of recon(s), comma separated (only FOR*,PAY*,LSC*,ESC* processed) :"
    inputvalue = raw_input()
    print "Please provide date for (YYYYMMDD):"
    inputdate = raw_input()
    cases = inputvalue.rsplit(',')

    for case in cases:
        inputvalue = case
        if inputvalue.startswith("LSC"):
            copyfile(path,reconlsc,inputdate,inputvalue,valuepath,reconmaps[reconlsc])
        elif inputvalue.startswith("PAY"):
            copyfile(path,reconpay,inputdate,inputvalue,valuepath,reconmaps[reconpay])
        elif inputvalue.startswith("FOR"):
            copyfile(path,reconfor[:-1],inputdate,inputvalue,valuepath,reconmaps[reconfor])
        if inputvalue.startswith("ESC"):
            copyfile(path,reconlsc,inputdate,inputvalue,valuepath,reconmaps[reconlsc])
        else:
            print "We do not process :",inputvalue


def copyfile(path, inboxvalue, inputdate, inputvalue, valuepath, lftptvalue):

    oldprefix="/mqsiarchive/old_"
    source = path + inboxvalue + oldprefix + inputdate + "/*" + inputvalue
    commandcopysource = glob.glob(source)
    commandcopytarget = valuepath + lftptvalue

    if len(commandcopysource) == 1:
        orginalname = commandcopysource[0].rsplit('/', 1)[-1]
        shutil.copy(commandcopysource[0],commandcopytarget)
        shutil.move(commandcopytarget+"/"+orginalname,commandcopytarget+"/"+inputvalue+"_")
    else:
        print "File :" + source +" not found for date :" + inputdate


if __name__ == "__main__":
    switcher = {
        1: "reconsrename",
        2: "delete",
        3: "lftptransferbackout",
        4: "Inbox.reconXYZ",
        5: "Dropped"
    }

    keypath = '/cs/mqsi/data/'
    valuepath = '/cs/mqsi/data/scripts/'
    reconmap = {
                "Inbox.recondepos": "recondepos/lftptransferbackout",
                "Inbox.reconpay": "reconpay/lftptransferbackout",
                "Inbox.LSVplus": "LSVPLUS/lftptransferbackoutput",
                "Inbox.PCESR": "PCESR/lftptransferbackout",
                "Inbox.reconlsc": "reconlsc/lftptransferbackout",
                "Inbox.reconipr": "reconipr/lftptransferbackout",
                "Inbox.reconlee": "reconlee/lftptransferbackout",
                "Inbox.reconcols": "reconcols/lftptransferbackout",
                "Inbox.reconlsc_": "reconesc/lftptransferbackout",
                "Inbox.reconivr": "reconivr/lftptransferbackout",
				"Inbox.reconpay_": "reconpay/lftptransferbackoutfor"
                }

    print("*********************************************************************************")
    print("********************************SPS SCANNING*************************************")
    print("Select Option :")
    print("1   Rename OK/NOK recons from lftptransferbackout")
    print("2   Delete particular file(s) on location X with pattern Y*")
    print("3   List source folders  lftptransferbackout")
    print("4   List destination Inbox.reconXYZ folders")
    print("5   Process Message Dropped")
    print("*********************************************************************************")

    inputChoice = input()
    value = switcher.get(inputChoice, 'Invalid choice')

if value == "reconsrename":
    reconsrename(reconmap,valuepath,keypath)
elif value == "delete":
    delete()
elif value == "lftptransferbackout":
    list_source_folder(reconmap,valuepath)
elif value == "Inbox.reconXYZ":
    list_destination_folder(reconmap, keypath)
elif value == "Dropped":
    process_message_dropped(reconmap, keypath, valuepath, reconmap)
else:
    print (value)