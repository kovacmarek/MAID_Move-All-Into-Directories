import os
import re
from pathlib import Path
import json

def undoCreate(chosen_folder, FileList):
    with open(chosen_folder + "\\" + "undo_temp.txt", "w+") as convert_file:
        convert_file.write(json.dumps(FileList))
        
    # Set hidden file
    os.system("attrib +h " + chosen_folder + "\\" + "undo_temp.txt")

def fetchFileTypes(chosen_folder):
    files = os.listdir(chosen_folder)
    FileList = []
    for file in files:
        result = re.search(r".*\.(\w*)", file)
        if (result != None): # Skip Folders
            if(result.string != "SortFiles.py" and result.string != "undo_temp.txt"): # Skip script & temp
                tempDict = {}
                tempDict["name"] = result.string
                tempDict["type"] = (result.group(1))  
                tempDict["origPath"] = chosen_folder + "\\" + result.string  
                FileList.append(tempDict)  
    if (FileList == []):
        FileList = None  
    return FileList

def createFolders(chosen_folder, FileList):
    FileTypes = []
    for file in enumerate(FileList): # Filter unique file type names
        FileTypes.append(FileList[file[0]]["type"])
    FileTypes = set(FileTypes)

    for file in FileTypes: # Create Folders
        if not(os.path.exists(chosen_folder + "\\" + file) and os.path.isdir(chosen_folder + "\\" + file)):
            os.makedirs(chosen_folder + "\\" + file)

def moveFilesToFolders(chosen_folder, FileList):
    # Manage & create existing "undo" file
    if os.path.exists(chosen_folder + "\\" + "undo_temp.txt"):
        os.remove(chosen_folder + "\\" + "undo_temp.txt")
        undoCreate(chosen_folder, FileList)
    else:
        undoCreate(chosen_folder, FileList)

    # Move Files
    for file in FileList:
        os.rename(chosen_folder + "\\" + file["name"], chosen_folder + "\\" + file["type"] + "\\" + file["name"])

def moveFilesUndo(chosen_folder, FileList):
    with open(chosen_folder + "\\" + "undo_temp.txt") as undo_list:
        data = json.load(undo_list)
        for file in data:
            os.rename(chosen_folder + "\\" + file["type"] + "\\" + file["name"], file["origPath"]) 
            print("Moved: " + file["name"] + " to " + file["origPath"])