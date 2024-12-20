import os
import shutil
from mutagen.mp4 import MP4

from datetime import datetime
from PIL import Image, ExifTags

imgExtensions = [".png", ".gif", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp"]
vidExtensions = [".mp4"]
inputPath = "./New folder/Camera"
outputPath = "./Output Folder/"

months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']

def getFolderContent(input_path):
    output= {'files': [], 'directories': []}
    for f in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, f)):
           output['files'].append(f)
        else: 
           output['directories'].append(f)
    
    return {'files': output['files'], 'directories': output['directories']}

def getFiles(input_path):
    content = getFolderContent(input_path)
    output = [f"{input_path}/{file}" for file in content["files"]]
    # output = f"{input_path}/{content['files']}"
    for dir in content['directories']:
        output = output + getFiles(os.path.join(input_path, dir))
    return output

def isImage(input_path):
    if(os.path.isdir(input_path) or os.path.isfile(input_path)):
        return os.path.splitext(input_path)[1] in imgExtensions
def isVideo(input_path):
    if(os.path.isdir(input_path) or os.path.isfile(input_path)):
        return os.path.splitext(input_path)[1] in vidExtensions

def getMetaData(input_path):
    output = {}
    if(isImage(input_path)):
        img = Image.open(os.path.abspath(input_path))
        output = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS } if img._getexif() else {}
    if(output == {}):
        output = getDateByName(input_path)
    return output
    
def getDateByName(input_path):
    if(input_path.find('_') == -1): return {}
    file_name_split = os.path.splitext(os.path.basename(input_path))[0].split('_')[0]
    if(file_name_split.isnumeric() and len(file_name_split) == 8):
        year = file_name_split[:4]
        month = file_name_split[4:6]
        day = file_name_split[-2:]
        if(int(day) <= 31 and int(month) <= 12):
            meta = '{0}:{1}:{2} 12:00:00'.format(year, month, day)
            return {"DateTime": meta}
        
    else: return {}
    
def createOutputDatePath(output_path, timestamp):
    yearPath = os.path.join(output_path, timestamp[:4])
    monthPath = os.path.join(yearPath, f'{timestamp[5:7]}-{months[int(timestamp[5:7])-1]}')
    if(not os.path.exists(output_path)): os.mkdir(output_path)
    if(not os.path.exists(yearPath)): os.mkdir(yearPath)
    if(not os.path.exists(monthPath)): os.mkdir(monthPath)
    return monthPath

for file in getFiles("./Sample"):
    if(not os.path.exists(outputPath)): os.mkdir(outputPath)

    sorted_output = os.path.join(outputPath, "cacamera_range")
    scrambled_output = os.path.join(outputPath, "cacamera_bazar")
    meta = getMetaData(file)
    if("DateTime" in meta):
        shutil.copyfile(file, os.path.join(createOutputDatePath(sorted_output, meta["DateTime"]), os.path.split(file)[1]))
    else:
        if(not os.path.exists(scrambled_output)): os.mkdir(scrambled_output)
        shutil.copyfile(file, os.path.join(scrambled_output, os.path.split(file)[1]))