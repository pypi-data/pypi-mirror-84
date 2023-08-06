#=============================================================
#=================     Library Import    =====================
#=============================================================

import traceback
# Importa a parte de Subprocesso

import logging

import os

from pathlib import Path

import datetime

#=============================================================
#=================        class          =====================
#=============================================================


# Classe LogAutomator Resposável pela automatização do processo usando o Log
class LogAutomator:

    # Application
    log_Prompt = 1
    
    log_File = 1

    #log_FileName = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent, "Logs" , "log_file_" + str(datetime.datetime.now().year) + "_"+ str(datetime.datetime.now().month)+"_"+ str(datetime.datetime.now().day) +".txt")

    def __init__(self):
        nothing = None
        #self.log_FileName = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent, "Logs" , "log_file_" + str(datetime.datetime.now().year) + "_"+ str(datetime.datetime.now().month)+"_"+ str(datetime.datetime.now().day) +".txt")

    def writeLog(self,logType, description):
        print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - " + logType + ' - ' + description)
        """if os.path.exists(LogAutomator.log_FileName) == False:
            logFile = open(LogAutomator.log_FileName , 'w+')
        else:
            logFile = open(LogAutomator.log_FileName , 'a')

        try:

            logging.disable(0)

            if logType == "INFO":
                logging.basicConfig(filename=LogAutomator.log_FileName, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.info(description)
                print('INFO - ' + description)

            if logType == "ERROR":
                logging.basicConfig(filename=LogAutomator.log_FileName, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.error(description)
                print('ERROR - ' + description)

            if logType == "DEBUG":
                logging.basicConfig(filename=LogAutomator.log_FileName, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.debug(description)
                print('DEBUG - ' + description)
        except:
            donothing = None
        finally:
            logFile.close()

        """
