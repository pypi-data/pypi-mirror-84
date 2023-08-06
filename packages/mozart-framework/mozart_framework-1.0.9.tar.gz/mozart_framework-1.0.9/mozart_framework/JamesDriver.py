# =============================================================
# =================     Library Import    =====================
# =============================================================

import requests
import socket
from mozart_framework.LogDriver import LogAutomator
from mozart_framework.QueueItem import QueueItem
import json
import sys

import jsonpickle

# =============================================================
# =================        class          =====================
# =============================================================

# Classe James Responsável pela a comunicação com o módulo do JAMES
class James:

    jamesUrl = "http://localhost:8092/james"
    headers = {'User-Agent': 'PostmanRuntime/7.20.1', 'sender': socket.gethostname() , 'Content-Type' : 'application/json'}
    logger = LogAutomator()
    processID = "INSERT YOUR PROCESS EXTERNAL-ID HERE"
    executionID = 0

    def __init__(self):
        counter = 0
        while len(sys.argv) > counter:
            if sys.argv[counter] == '--execid':
                try:
                    self.executionID = sys.argv[counter + 1]
                except:
                    self.executionID = 0
                break
            counter = counter + 1

    def send_report_file(self, id, description, fileDirectory, fileName):

        if id != 0:
            self.logger.writeLog('INFO',
                                 'Performing POST Request on: '+ self.jamesUrl + "/v1/report/create/" + str(id))

            files = {"file": (fileName, open(fileDirectory, 'rb')),
                     "description": (None, description)
                     }
            print(str(id))
            endpoint = self.jamesUrl+"/v1/report/create/" + str(id)
            self.logger.writeLog('INFO',
                                 'Performing POST Request on: '+endpoint)

            resp = requests.post(endpoint, files=files)
            if resp.status_code != 200:
                self.logger.writeLog('ERROR',
                                     'POST Request on ' + self.jamesUrl + "/v1/report/create/" + str(id)+
                                     " FAILED with the following status " + ' {}'.format(resp.status_code))
                raise Exception('ERROR',
                    'POST Request on ' + self.jamesUrl + "/v1/report/create/" + str(id) +
                    " FAILED with the following status " + ' {}'.format(resp.status_code))
            return resp.content.decode()
        else:
            return "Error"

    def get_next_item(self, queue_name, size):

        self.logger.writeLog('INFO' , 'Performing GET Request on ' + self.jamesUrl + "/v1/queue/get-next-items/" + queue_name +"/items/" + str(size) +
                           " with the following Headers " + str(self.headers) +
                            " with no Request Body")

        resp = requests.get(self.jamesUrl + "/v1/queue/get-next-items/" + queue_name +"/items/" + str(size) ,
                             headers=self.headers)

        if resp.status_code != 200:
            self.logger.writeLog('ERROR', 'GET Request on ' + self.jamesUrl + "/v1/queue/get-next-items/" + queue_name + "/items/" + str(size) +
                                 " FAILED with the following status " + ' {}'.format(resp.status_code))

            raise Exception('GET Request on ' + self.jamesUrl + "/v1/queue/get-next-items/" + queue_name + "/items/" + str(size) +
                                 " FAILED with the following status " + ' {}'.format(resp.status_code))

        jsondata = resp.json()
        queueitemlist = []

        while jsondata:
            item = QueueItem(jsondata[0]['id'] , jsondata[0]['name'] , jsondata[0]['priority'] , jsondata[0]['status'] , jsondata[0]['content'])
            queueitemlist.append(item)
            jsondata.pop()

        return queueitemlist


    def update_item_status(self, queue_name: str, queue_item: QueueItem):

        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)

        jpi = jsonpickle.encode(queue_item)
        jsonObj = json.loads(jpi)

        self.logger.writeLog('INFO' , 'Performing PUT Request on ' + self.jamesUrl + "/v1/queue/update-item/" + queue_name +"/items/" + str(queue_item.id) +
                           " with the following Headers: " + str(self.headers) +
                            " with the following Request Body " + str(jsonObj))

        resp = requests.put(self.jamesUrl + "/v1/queue/update-item/" + queue_name +"/items/" + str(queue_item.id) ,
            headers=self.headers, json=jsonObj)

        if resp.status_code != 200:
            self.logger.writeLog('ERROR', 'PUT Request on ' + self.jamesUrl + "/v1/queue/update-item/" + queue_name +"/items/" + str(queue_item.id) +
                                 " FAILED with the following status " + ' {}'.format(resp.status_code))

            raise Exception('PUT Request on ' + self.jamesUrl + "/v1/queue/update-item/" + queue_name +"/items/" + str(queue_item.id) +
                                 " FAILED with the following status " + ' {}'.format(resp.status_code))

        return resp.json()

    def create_item_queue(self, queue_name: str, queue_item: QueueItem):

        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)

        jpi = jsonpickle.encode(queue_item)
        jsonObj = json.loads(jpi)

        self.logger.writeLog('INFO',
                             'Performing POST Request on ' + self.jamesUrl + "/v1/queue/create-item/" + queue_name + "/" +
                             " with the following Headers: " + str(self.headers) +
                             " with the following Request Body " + str(jsonObj))

        resp = requests.post(self.jamesUrl + "/v1/queue/create-item/" + queue_name + "/",
                            headers=self.headers, json=jsonObj)

        if resp.status_code != 200:
            self.logger.writeLog('ERROR',
                                 'POST Request on ' + self.jamesUrl + "/v1/queue/create-item/" + queue_name + "/" +
                                 " FAILED with the following status " + ' {}'.format(resp.status_code))

            raise Exception('POST Request on ' + self.jamesUrl + "/v1/queue/create-item/" + queue_name + "/" +
                            " FAILED with the following status " + ' {}'.format(resp.status_code))

        return resp.text


    def get_process_info(self):

        self.logger.writeLog('INFO',
                             'Performing GET Request on ' + self.jamesUrl + "/v1/process/external/" + self.processID +
                             " with the following Headers " + str(self.headers) +
                             " with no Request Body")

        resp = requests.get(self.jamesUrl + "/v1/process/external/" + self.processID,
                            headers=self.headers)

        if resp.status_code != 200:
            self.logger.writeLog('ERROR',
                                 'GET Request on ' + self.jamesUrl + "/v1/process/external/" + self.processID +
                                 " FAILED with the following status " + ' {}'.format(resp.status_code))

            raise Exception(
                'GET Request on ' + self.jamesUrl + "/v1/process/external/" + self.processID +
                " FAILED with the following status " + ' {}'.format(resp.status_code))

        return resp.json()

    def return_execution_status(self,status, errorMessage):

        if self.executionID != 0:

            json = {"status" : status, 'errorMessage' : errorMessage}

            self.logger.writeLog('INFO',
                                 'Performing PUT Request on ' + self.jamesUrl + "/v1/execution/last-run-time/" + str(self.executionID) +
                                 " with the following Headers: " + str(self.headers) +
                                 " with the following Request Body " + str({"status" : status, 'errorMessage' : errorMessage}))

            resp = requests.put(self.jamesUrl + "/v1/execution/last-run-time/" + str(self.executionID),
                                headers=self.headers, json=json)

            if resp.status_code != 200:
                self.logger.writeLog('ERROR',
                                     'PUT Request on ' + self.jamesUrl + "/v1/execution/last-run-time/" + str(self.executionID) +
                                     " FAILED with the following status " + ' {}'.format(resp.status_code))

                raise Exception('PUT Request on ' + self.jamesUrl + "/v1/execution/last-run-time/" + str(self.executionID) +
                                " FAILED with the following status " + ' {}'.format(resp.status_code))

            return resp.json()
