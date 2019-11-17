#Author-woodenCaliper
#Description-fusion360がアップデートをするたびにexeのファイルパスが変わり、そのたびにlogicoolのプロファイルのリンクを修正する作業を自動化

import adsk.core, adsk.fusion, adsk.cam, traceback

import xml.etree.ElementTree as ET
import glob
import shutil, datetime


def serchTargetFile():
    # logicoolのプロファイルのファイルパスをリストで取得
    logicoolProfileList = glob.glob(r"C:\Users\*\AppData\Local\Logitech\Logitech Gaming Software\profiles\*.xml")

    targetFile = 0
    oldFusionPath = 0
    # Fusionが対象のプロファイルを探す
    for profileFilePath in logicoolProfileList:
        xmlTree = ET.parse(profileFilePath)

        root = xmlTree.getroot()
        rootTag = root.tag
        ns = "{"+rootTag[rootTag.index("{") + 1:rootTag.rindex("}")] +"}"
        
        profilesTag = root

        profileTag =0
        for i in profilesTag.iter(ns+"profile"):
            profileTag = i

        print(profileTag.attrib["name"])

        targetTag=0
        for i in profileTag.iter(ns+"target"):
            targetTag=i

        if targetTag!=0:
            print(targetTag.attrib["path"])

            gamePath = targetTag.attrib["path"]
            if "Fusion360.exe" in gamePath:
                targetFile = profileFilePath
                oldFusionPath = targetTag.attrib["path"]

                return (targetFile, oldFusionPath)
    return (None, None)


def replaceFusionPath(targetFile, oldFusionPath):
    newFusionPath = glob.glob(r"C:\Users\*\AppData\Local\Autodesk\webdeploy\production\*\Fusion360.exe")
    newFusionPath = newFusionPath[0]

    if oldFusionPath != newFusionPath:
        # backup
        now = datetime.datetime.today().strftime("%Y_%m_%d_%Hh%Mm%Ss")
        shutil.copyfile(targetFile, targetFile + now)

        with open(targetFile, encoding="utf-8") as f:
            dataLines = f.read()
        with open(targetFile, encoding="utf-8", mode="w") as f:
            dataLines = dataLines.replace(oldFusionPath, newFusionPath)
            f.write(dataLines)
        return newFusionPath
    return False


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        (targetFile, oldFusionPath) = serchTargetFile()
        newFusionPath = replaceFusionPath(targetFile, oldFusionPath)

        if newFusionPath:
            ui.messageBox(
                "Change success" +"\n"
                + "\n"
                + oldFusionPath +"\n"
                +"↓"+"\n"
                + newFusionPath
            )
        else:
            ui.messageBox("No need change")
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))