from Patient import Patient
import uuid
class Hospital:
    def __init__(self, name, capacity):
        self.ID= "hos-"+str(uuid.uuid1())
        self.name = name
        self.capacity = int (capacity) 
        self.patients = [] # List of patients admitted to the hospital 
        self.staff = [] # List of doctors and nurses working in the hospital
    
    # return the percentage of occupancy of this hospital 
    def occupancy (self):         
        return "{:.3f}".format(100* len(self.patients) / self.capacity)
    
    
    
    # admit a patient to the hospital of given name and date of birth 
    def admission (self, name, dob):         
        p = Patient (name, dob)
        p.monitoredIn = self.ID
        self.patients.append(p)
        return p
            
    
    
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
    
    
    
    def serializeExtended(self): #for the hospitalInfo function in CovidAPI.py
        serialization = self.serialize()
        serialization["patients"] = [patient.serialize() for patient in self.patients]
        serialization["staffList"] = [staff.serialize()for staff in self.staff]
        return serialization
    
    
    
    def serializeSimplified(self):
        return {
                "id":str(self.ID),
                "occupancy":f"{self.occupancy()}%({len(self.patients)})"
        }
