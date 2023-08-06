import json

class QueueItem:
    id = ""
    name = ""
    priority = "MEDIUM"
    content = json.dumps({})

    def __init__(self):
        nothing = None



    def create_item(self,  name, priority ,  content, status=None , id= None):

        self.name = name
        self.priority = priority
        self.content = content
        if status != None:
            self.status = status
        if id != None:
            self.id = id



