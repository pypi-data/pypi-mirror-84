#=============================================================
#=================     Library Import    =====================
#=============================================================
from distutils.log import Log
from subprocess import Popen
# Importa a parte de Subprocesso

from pywinauto import Desktop

from pywinauto.controls.uiawrapper import UIAWrapper
# Importa o pywinauto

import time

from mozart_framework.LogDriver import LogAutomator

#=============================================================
#=================        class          =====================
#=============================================================
import pywinauto

# Classe UIAutomator Resposável pela automatização do processo usando a interface de desktop
class UIAutomator:

    # Application
    application = UIAWrapper

    logger = LogAutomator()


    # Abre o programa necessário e pega o windowTitle e a className
    def openProgram(self,programPath):
        Popen(programPath, shell=True)

    def assignWindowThatContainsNameToObject(self, windowTitle):
        windowList = Desktop(backend="uia").windows()
        windowFound = False
        print("Available Window List:" + str(windowList))
        for window in windowList:
            if windowTitle in str(window):
                self.application = window
                self.application.maximize()
                windowFound = True
                self.logger.writeLog("INFO",
                                     "Tela "+ str(window) +" Encontrada com Sucesso ")
                break
        print ("Window Found:" + str(windowFound))
        return windowFound

    def getWindowFullName(self, windowTitle):
        windowList = Desktop(backend="uia").windows()
        windowName = ""
        for window in windowList:
            if windowTitle in str(window):
                windowName = str(window).replace('uiawrapper.UIAWrapper', '')
                windowName = windowName.replace("'", '')
                windowName = windowName.replace(" - ",'', 1)
                windowName = windowName.replace(", Dialog", '')
                break
        print("Window Found: " + windowName)
        return windowName

    # Clica em um objeto realizando uma busca no window_wrapper já atualizado previamente pelo updateWindowWrapper
    def clickInput(self,objTitle, objControlType):
        childObjectList = self.application.descendants()
        print("Searching (" + objTitle +"-" + objControlType + ") in descendants list:")

        objectFound = False

        for object in childObjectList:
            if objTitle in str(object) and objControlType in str(object):
                objectFound = object
                break

        if objectFound != False:
            objectFound.click_input()

        self.logger.writeLog("INFO", "Object (title:" + str(objTitle) + ", control_type:" + str(
            objControlType)+ ") clicked with success.")

    def clickInputArrPos(self,objTitle, objControlType,pos):
        childObjectList = self.application.descendants()

        print("Searching (" + objTitle + "-" + objControlType + " in position " + str(pos) + ") in descendants list:")

        objectFound = False

        i = 0
        for object in childObjectList:
            if objTitle in str(object) and objControlType in str(object):
                i = i + 1
                if i == pos :
                    objectFound = object
                    break

        if objectFound != False:
            objectFound.click_input()

        self.logger.writeLog("INFO", "Object (title:" + str(objTitle) + ", control_type:" + str(
            objControlType)+ ") clicked with success.")

    def waitWindowDesccendantExists(self, window ,applicationTitle, maxretry=4):
        print("Waiting Window Descendant (" + window + "-" + applicationTitle + ") in descendants list:")

        objectFound = False
        for i in range(maxretry):
            childObjectList = self.application.descendants()

            for object in childObjectList:
                if window in str(object):
                    self.application = object
                    objectFound = True
                    break

            if objectFound== True:
                break
            else:
                time.sleep(1)
                self.assignWindowThatContainsNameToObject(applicationTitle)
        self.logger.writeLog("INFO", "Window: " + window + " " + str(objectFound))
        return objectFound

    # Digita em um objeto realizando uma busca no window_wrapper já atualizado previamente pelo updateWindowWrapper
    def typeKeysOnObject(self,objTitle, objControlType, textToType):
        childObjectList = self.application.descendants()

        print("Searching (" + objTitle + "-" + objControlType + ") in descendants list:")

        objectFound = False

        for object in childObjectList:
            if objTitle in str(object) and objControlType in str(object):
                objectFound = object
                break

        if objectFound != False:
            objectFound.type_keys(textToType, with_spaces=True)

        self.logger.writeLog("INFO", "Text: " + str(textToType) + " typed in Object (title:" + str(
            objTitle) + ", control_type:" + str(objControlType) + ") with success.")

    # Seleciona um item na combobox realizando uma busca no window_wrapper já atualizado previamente pelo updateWindowWrapper
    def selectItemOnComboBox(self, objTitle, objControlType, textToSelect):
        childObjectList = self.application.descendants()

        print("Searching (" + objTitle + "-" + objControlType + " ) in descendants list:")

        objectFound = False

        for object in childObjectList:
            if objTitle in str(object) and objControlType in str(object):
                objectFound = object
                self.logger.writeLog("INFO" , 'CBX_ITEMS:'+str(objectFound.item_count()))
                self.logger.writeLog("INFO", 'CBX_ITEMS:' + str(objectFound.texts()))
                break

        if objectFound != False:
            objectFound.select(textToSelect)

        self.logger.writeLog("INFO", "Item: " + str(textToSelect) + " selected in ComboBox (title:" + str(objTitle) + ", control_type:" + str(objControlType) + ") with success.")

    # Imprime todos os controles presentes da tela atual
    def printAllControlsForCurrentWindow(self):
        print(self.application.descendants())

    # fecha a última tela ativa
    def closeActiveWindow(self):
        self.application.wrapper_object().close()
        
