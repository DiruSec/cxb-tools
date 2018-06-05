#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
from urllib.request import urlopen

APP_BASE_DIR = "64_06_4B66B35C"
BASE_URL = "https://cxb-dl.ac.capcom.jp"
STATIC_FILES = ["config/config_11600.json"]

def downloadProgress(bytes_so_far, total_size, currentFile):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("\r" + currentFile + "...%d%%" % percent)

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

def downloadFile(url, currentFile):
    response = urlopen(url)
    totalsize = int(response.headers['Content-Length'].strip())
    bytes_so_far = 0
        
    while 1:
        file = response.read(8192)
        bytes_so_far += len(file)
    
        if not file:
            break
    
        downloadProgress(bytes_so_far, totalsize, currentFile)

    return file

def savePath(path):
    return "resource/"+path

def makeSave(path):
    os.makedirs(os.path.dirname(savePath(path)), exist_ok=True)

    if os.path.exists(savePath(path)):
        print(path+"... Skipped.")
        return

    saveFile = open(savePath(path),"w+b")
    try:
        saveFile.write(downloadFile(BASE_URL+'/'+path, path))
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print(path+"... Failed.")
    saveFile.close

with open("download_file_list.txt", "r") as f:
    DownloadList = f.read().splitlines()
    for files in DownloadList:
        makeSave(files)
    for files in STATIC_FILES:
        makeSave(files)


