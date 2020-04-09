import uuid
class Patient:
    def __init__(self, name, dob):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob
        self.status = "Undiagnosed"
        self.monitoredIn = None
        
        
    
    def changeAttribute (self, attribute, newVal):
        if attribute == "status":
            self.status = newVal
        elif attribute == "monitoredIn":
            self.monitoredIn = newVal
        return self    
    
        
    
        
    def serialize(self):
       return  {"id":self.ID,
                "name":self.name,
                "dob":self.dob,
                "status":self.status,
                "monitored":self.monitoredIn
                }
       
    
    def serializeSimplified(self):
        return {"id":self.ID,
                "status":self.status}
