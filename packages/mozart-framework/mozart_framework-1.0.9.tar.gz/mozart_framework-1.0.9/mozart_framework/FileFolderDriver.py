#=============================================================
#=================     Library Import    =====================
#=============================================================

import os
# Importa OS
import shutil
# Importa Shutil


#=============================================================
#=================        class          =====================
#=============================================================

# Classe FileFolderAutomator Resposável pela automatização do processo usando interações de pastas
class FileFolderAutomator:

    def createFolder(folderPath):
        os.makedirs(folderPath)

    def deleteFolder(folderPath):
        shutil.rmtree(folderPath)

    def deleteFile(filePath):
        os.unlink(filePath)

    def checkFileExists(filePath):
        return(os.path.exists(filePath))

    def copyFile(sourcePath, targetPath):
        if FileFolderAutomator.checkFileExists(targetPath) == True:
            FileFolderAutomator.deleteFile(targetPath)
        shutil.copy(sourcePath,targetPath)

    def deleteAllFilesOnFolder(folderPath):
        for filename in os.listdir(folderPath):
            FileFolderAutomator.deleteFile(os.path.join(folderPath, filename))

    def createFile(FilePath):
        file = open(FilePath, 'w+')
        file.close()

    def killprocess(processName):
        os.system("taskkill /im "+processName)