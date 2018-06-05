#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys, getopt, urllib.request

APP_BASE_DIR = "64_06_4B66B35C"
BASE_URL = "https://cxb-dl.ac.capcom.jp"
STATIC_FILES = ["config/config_11600.json"]

def downloadProgress(currentBytes, totalSize, currentFile):

    percent = float(currentBytes) / totalSize
    percent = round(percent*100, 2)
    sys.stdout.write("\r" + currentFile + "...%d%%" % percent)

    if currentBytes >= totalSize:
        sys.stdout.write('\n')

def downloadFile(url, currentFile):
    if (proxyPath != False):
        proxy = urllib.request.ProxyHandler({'http' : 'http://' + proxyPath, 'https': 'https://' + proxyPath})
        urllib.request.install_opener(urllib.request.build_opener(proxy))

    response = urllib.request.urlopen(url)
    totalsize = int(response.headers['Content-Length'].strip())
    currentBytes = 0
    fileObject = b''
        
    while 1:
        file = response.read(8192)
        fileObject += file
        currentBytes += len(file)
    
        if not file:
            break

        downloadProgress(currentBytes, totalsize, currentFile)
    
    return fileObject

def savePath(path):
    return "resource/"+path

def makeSave(path):
    os.makedirs(os.path.dirname(savePath(path)), exist_ok=True)

    if os.path.exists(savePath(path)):
        print(path+"... Skipped.")
        return

    with open(savePath(path),"w+b") as saveFile:
        try:
            saveFile.write(downloadFile(BASE_URL+'/'+path, path))
            saveFile.close()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(path+"... "+str(e))

def checkProxy():
    opts, args = getopt.getopt(sys.argv[1:], "p:")
    for op, value in opts:
        if op == "-p":
            print ("Using proxy %s"%value)
            return value
    return False

with open("download_file_list.txt", "r") as f:
    DownloadList = f.read().splitlines()
    proxyPath = checkProxy()
    for files in DownloadList:
        files = APP_BASE_DIR + '/' + files
        makeSave(files)
    for files in STATIC_FILES:
        makeSave(files)


