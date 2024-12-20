import os
import shutil
from datetime import datetime
from PIL import Image, ExifTags
import numpy as np
from file_management import createOutputDatePath, getDateByName, getFiles, getMetaData

imgExtensions = [".png", ".gif", ".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp"]
inputPath = "./New folder/Camera"
outputPath = "./Output Folder/"

months = ['janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre']

input_file_list = getFiles("./Sample")
for file in input_file_list:
    if(not os.path.exists(outputPath)): os.mkdir(outputPath)
    sorted_output = os.path.join(outputPath, "cacamera_range")
    scrambled_output = os.path.join(outputPath, "cacamera_bazar")
    meta = getMetaData(file)
    if("DateTime" in meta):
        shutil.copyfile(file, os.path.join(createOutputDatePath(sorted_output, meta["DateTime"]), os.path.split(file)[1]))
    else:
        if(not os.path.exists(scrambled_output)): os.mkdir(scrambled_output)
        shutil.copyfile(file, os.path.join(scrambled_output, os.path.split(file)[1]))
output_file_list = getFiles(outputPath)
print(np.setdiff1d(input_file_list, output_file_list))

