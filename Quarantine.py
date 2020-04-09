
import uuid
class Quarantine:
    def __init__(self, name, capacity):
        self.ID = "quar-"+str(uuid.uuid1())
        self.name = name
        self.capacity = int(capacity)
        self.patients = []
        self.staff = []

    def occupancy(self):
        return "{:.3f}".format(100* len(self.patients) / self.capacity)

        
    
    
    def admitStaff(self, employee):
        self.staff.append(employee)
     
    
    
    
    def serialize(self):
        return {
                    'id': str(self.ID), 
                    'name': self.name, 
                    'capacity': self.capacity,
                    'occupancy': f"{self.occupancy()}%({len(self.patients)})",
                    "staff":len(self.staff)
                
                }
   
    
    
    
    def serializeExtended(self):#for the hospitalInfo function in CovidAPI.py
        serialization = self.serialize()
        serialization["patients"] = [patient.serialize() for patient in self.patients]
        serialization["staffList"] = [staff.serialize()for staff in self.staff]
        return serialization
    
    
    
    
    
    def serializeSimplified(self):
        return {"id":str(self.ID),
                "occupancy":f"{self.occupancy()}%({len(self.patients)})"
                }
        
        
