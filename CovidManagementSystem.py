from Hospital import *
from Quarantine import *
from Staff import *
import pickle
from os import path
import random

class CovidManagementSystem:
    def __init__(self):
        self.hospitals = self.getDataFromFile("hospitals.obj")
        self.quarantines = self.getDataFromFile("quarantines.obj")
        self.allEmployees = self.getDataFromFile("staff.obj")
        self.allPatients = self.getDataFromFile("patients.obj")



    """"
        Functions for hospitals
    """    
    def getHospitals(self):
        return self.hospitals


    def addHospital(self, name, capacity):
        h = Hospital(name, capacity)
        self.hospitals.append(h)
        self.saveToFile("hospitals.obj", self.hospitals)
        return True,f"Added a new hospital called {name} with capacity {capacity}"
        

    
    """"
        Functions for patients
    """  
            
    def getPatient(self, patId_, facility):
        patId_ = patId_.strip("<>")
        for patient in facility:
            if patient.ID == patId_:
                return patient   
        return None   
   
    
    
    def createNewPatient(self, name, dob):
        newP = Patient(name, dob)
        self.allPatients.append(newP)
        self.saveToFile("patients.obj", self.allPatients)
        return True, f"Patient with name:{name} and dateOfBirth:{dob} was added to the system!"
     
        
    
    
    def discharge(self, pat_id, facility_id):
        facility = self.getFacilityById(facility_id)
        if facility != None:
           patient = self.getPatient(pat_id, facility.patients)
           if patient != None:
               if(patient.status == "infected"):
                   return False, f"Patient with id:{pat_id} can't be discharged since he/she is infected!"
               patientFromAllPatients = self.getPatient( pat_id, self.allPatients )
               patientFromAllPatients.changeAttribute("monitoredIn", None)
               patientFromAllPatients.changeAttribute("status","discharged")
               facility.patients.remove(patient)
               facilityFile = "hospitals.obj" if facility_id.startswith("hos") else "quarantines.obj"
               facilityType = self.hospitals if facility_id.startswith("hos") else self.quarantines
               self.saveToFile(facilityFile, facilityType, saveToSecondFile="patients.obj", theSecondObject=self.allPatients)
               return True, f"Patient with id:{patient.ID} was discharged from facility with id:{facility.ID}"
           else:
               return False, f"Patient with id:{pat_id} not found inside the facility with id:{facility_id}"
        return False, f"Facility with id :{facility_id} not found!"
    


    def diagnose(self, pat_id): 
        patient = self.getPatient(pat_id, self.allPatients)
        test = random.randint(0,101)
        pat_id = pat_id.strip("<>")
        if test <= 90 and patient != None:
            patient.status = "discharged"
            if patient.monitoredIn != None:
                self.discharge(pat_id, patient.monitoredIn)
            return True, f"Patient with id:{patient.ID} tested negative and was discharged"
        elif test > 90 and patient != None:
            patient.status = "infected"
            transfer = self.transferPatientToAnyQuarantine(pat_id, self.quarantines)
            self.saveToFile("hospitals.obj", self.hospitals, saveToSecondFile="quarantines.obj",theSecondObject=self.quarantines)
            self.saveToFile("patients.obj", self.allPatients)
            return transfer if transfer != None else (True,f"Patient tested positive")
        
        return False, f"Patient with id:{pat_id}not found"
            
     
        
    def cure(self, pat_id): 
        patient = self.getPatient(pat_id, self.allPatients)
        cure = random.randint(0, 101)
        if patient.status == "infected":
            if cure <= 97 and patient != None:
                patient.status = "discharged"
                self.discharge(pat_id.strip("<>"), patient.monitoredIn)
                return True,f"Patient with id :{pat_id} was cured successfully and was discharged!"
            else:
                patient.status = "dead"
                if patient.monitoredIn != None:
                    #even here the patient will be discharge or in this case removed from the hospital
                    self.discharge(pat_id.strip("<>"), patient.monitoredIn)
                return True,f"Patient with id: {pat_id} unfortunately couldn't get cured and as a result died!"
        
        elif patient.status == "Undiagnosed":
            return False,f"The process of curing can not start on the patient with id:{pat_id}, because the patient is undiagnosed!"
        elif patient.status == "discharged":
            return False,f"The process of curing can not start on the patient with id:{pat_id}, because the patient is already discharged!"
        else:
            return False,f"Patient with id:{pat_id} is unfortunately dead!"
        
        return False,f"Patient with id:{pat_id} not found!"
    
    
    
    
    def admitPatientF(self, fac_id, pat_id): 
        p = self.getPatient(pat_id, self.allPatients)
        currentFacId = None
        facToTransfer = self.getFacilityById(fac_id)
        facToTransferType = self.hospitals if fac_id.startswith("hos") else self.quarantines
        if p!= None and facToTransfer != None and float(facToTransfer.occupancy()) < 100.0:
            if p.monitoredIn != None:
                if p.monitoredIn == fac_id.strip("<>"):
                    return False, f"Patient is already in the specified facility"
                currentFac = self.getFacilityById( p.monitoredIn )
                currentFacId = currentFac.ID
                currentFacType = self.hospitals if p.monitoredIn.startswith("hos") else self.quarantines
                patientInFacility = self.getPatient(pat_id, currentFac.patients)
                currentFac.patients.remove(patientInFacility)    
            p.changeAttribute("monitoredIn", facToTransfer.ID)
            facToTransfer.patients.append(p)
            self.saveToFile("hospitals.obj", self.hospitals, saveToSecondFile="quarantines.obj",theSecondObject=self.quarantines)
            self.saveToFile("patients.obj", self.allPatients)
            return True, f"patient with id {pat_id} was transfered to facility with id:{facToTransfer.ID}"
        elif facToTransfer != None and float(facToTransfer.occupancy() >= 100.0):
            return False, f"Facility with id:{fac_id} has not enough capacity left to accomodate the patient!"
        elif facToTransfer == None:
            return False, f"Facility not found!"
        return False,f"Patient not found"
           
    
    
    
     #used by the diagnose function
    def transferPatientToAnyQuarantine(self, pat_id, facilityTypeToTransfer):
        patient = self.getPatient(pat_id, self.allPatients)
        #First condition is check if the patient is already in a hospital, if yes remove it from the hospital
        if patient.monitoredIn != None and patient.monitoredIn.startswith("hos"):
            facility = self.getFacilityById(patient.monitoredIn)
            patientInFacility = self.getPatient(pat_id, facility.patients)
            facility.patients.remove(patientInFacility)
        
        #here is if patient is already in a quarantine just return because there is no need to transfer him/her to a quarantine    
        elif patient.monitoredIn != None and patient.monitoredIn.startswith("quar"):
            return None
        
        #this transfers the patient to the first quarantine that has enough capacity
        #this runs always unless the elif condition is met in that case as mentioned...
        #there is no need to do a transfer
        for fac in facilityTypeToTransfer:
            if float(fac.occupancy()) < 100.0: 
                patient.monitoredIn = fac.ID
                fac.patients.append(patient)
                return True, f"Patient {pat_id} tested positive and was quarantined to the quarantine with the id:{fac.ID}!"
         
        return False, f"Patient Not Found"  
    
    
    
    
    
    
    """"
        Functions for staff
    """  
    
    def getEmployee(self, employeeId, theList):
        employeeId = employeeId.strip("<>")
        for employee in theList:
            if employee.ID == employeeId:
                return employee      
        return None
    



    def deleteEmployee(self, employeeId):
         employee = self.getEmployee(employeeId, self.allEmployees)
         if employee != None:
             self.allEmployees.remove(employee)
             if employee.worksIn != None:
                 facilityFile = "hospital.obj" if employee.worksIn.startswith("hos") else "quarantine.obj"
                 facilityType = self.hospitals if employee.worksIn.startswith("hos") else self.quarantines
                 workPlace = self.getFacilityById(employee.worksIn)
                 employeeToDelete = self.getEmployee(employeeId, workPlace.staff)
                 workPlace.staff.remove(employeeToDelete)
                 self.saveToFile(facilityFile, facilityType, saveToSecondFile="staff.obj", theSecondObject=self.allEmployees)
             return  True,f"Employee with the position:{employee.position} and id:{employee.ID} was deleted from the system!"
         return False, f"Employee with id:{employeeId} not found!" 
            
            
                      
            
    def assignEmployee(self, employeeId, facilityId):
        employee = self.getEmployee(employeeId, self.allEmployees)
        formerWorkPlaceId = None
        if employee.worksIn != None:
            currentWorkPlaceId = employee.worksIn
            formerWorkPlaceId = currentWorkPlaceId
            currentWorkPlace = self.getFacilityById(currentWorkPlaceId)
            employeeToDelete = self.getEmployee(employeeId, currentWorkPlace.staff)
            currentWorkPlace.staff.remove(employeeToDelete)    
        newWorkPlace = self.getFacilityById(facilityId)
        if newWorkPlace != None:
            employee.worksIn = newWorkPlace.ID
            currentWorkPlaceId = employee.worksIn
            newWorkPlace.staff.append(employee)
            self.saveToFile("hospitals.obj", self.hospitals, saveToSecondFile="quarantines.obj", theSecondObject = self.quarantines)
            self.saveToFile("staff.obj", self.allEmployees)
            return True, f"Staff Member with id({employeeId}) has changed workplaces from:{formerWorkPlaceId} to:{currentWorkPlaceId}"
        else:
            return False, f"Facility with id:{facilityId} not found!"
        return False, f"Patient not found"
        
        

    def addStaff(self, name, dob, position):
        newEmployee = Staff(name, dob, position)
        self.allEmployees.append(newEmployee)
        self.saveToFile("staff.obj", self.allEmployees)
        return True, f"New staff member with name:{name}, dateOfBirth:{dob} and position:{position} was added to the system!"
        
    
    
    
    def getAllEmployees(self):
        return self.allEmployees






    """"
        Functions for quarantines
    """  

    def getQuarantines(self):
       return self.quarantines
    
    
    
    def addQuarantine(self, name, capacity):
        q = Quarantine(name, capacity)
        self.quarantines.append(q)
        self.saveToFile("quarantines.obj", self.quarantines)
        return True,f"Added a new quarantine area called {name} with capacity {capacity}"
    
    
         
    
    def deleteQuarantine(self, quarId):
        quarToDelete = self.getFacilityById(quarId)
        if quarToDelete == None:
            return False, "Facility not found!"
        
        patientsOfQuar = quarToDelete.patients
        numOfPatients = len(patientsOfQuar)
        if numOfPatients == 0:
                self.deleteFacility(quarId)
                self.saveToFile("quarantines.obj",self.quarantines, saveToSecondFile="patients.obj", theSecondObject=self.allPatients)
                return True, f"Quarantine {quarId} was successfully deleted"
        
        #the process of emptying the quarantine by transfering the patients to other quarantines
        for quarantine in self.quarantines:
            if quarantine != quarToDelete: #skip the quarantine we want to delete
                capacityLeft = quarantine.capacity - len(quarantine.patients)
                if capacityLeft == 0: #if the current quarantine doesnt have any capacity left, skip it
                    continue
                elif capacityLeft >= numOfPatients:
                    """
                        if the quarantine has enough capacity left to take all the patients 
                        of the quarantine that needs to be deleted, 
                        then store all the patients here!
                        first change the attribute monitoredIn of all patients to the new quarantineId
                    """
                    patientsInAllPatients = [self.getPatient(pat.ID, self.allPatients) for pat in patientsOfQuar]
                    patientsToTransferModified = [patient.changeAttribute("monitoredIn",quarantine.ID) for patient in patientsInAllPatients]
                    quarantine.patients.extend(patientsToTransferModified)
                    patientsOfQuar.clear()
                    return self.deleteQuarantine(quarToDelete.ID)
                elif self.totalCapacityLeftInFacilities(self.quarantines) >= numOfPatients:
                    patientsToTransfer = [patientsOfQuar[i] for i in range(0,capacityLeft)]
                    patientsInAllPatients = [self.getPatient(pat.ID, self.allPatients) for pat in patientsToTransferModified]
                    patientsToTransferModified = [patient.changeAttribute("monitoredIn",quarantine.ID) for patient in patientsInAllPatients]
                    quarantine.patients.extend(patientsToTransferModified[:capacityLeft])
                    for patient in range(0,capacityLeft):
                        patientsOfQuar.pop(patient)
                    return self.deleteQuarantine(quarToDelete.ID)    
                    """
                        If the quarantine we're currently are in the loop doesn't have 
                        enough capacity to take all the patients or maybe no capacity at all,
                        check first if the joint capacity of all other quarantines is enough,
                        to store all the patients, if yes then, store as many patients
                        as the current quarantine allows(by using the capacityleft variable
                        which if it is 0 then no patient will be stored in the current quarantine),
                        and delete the same number of patients from the quarantine 
                        which will be deleted as the number of patients added to the current quarantine.
                        
                        Repeat the process until the recursion is stopped by the 
                        second if statement of this function
                        
                    
                    """
        return False, f"Quarantine could not be deleted since there is not enough total capacity in other quarantines!"       
    
    
    def capacityLeftOfAllQuarantines(self):
        capacityLeft = 0
        for i in self.quarantines:
            capacity_i_Left = i.capacity - len(i.patients)
            capacityLeft += capacity_i_Left
        return capacityLeft 
    
    
    
    
    
    
    """"
        Function for stats
    """  
    
    def systemStats(self):
        numOfInfected = 0
        percentageOfInfected = 0
        for patient in self.allPatients:
            if patient.status == "infected":
                numOfInfected += 1
        if len(self.allPatients) != 0:        
            percentageOfInfected = "{:.2f}".format(numOfInfected / len(self.allPatients) * 100)
            
        statusOfFacilities = [facility.serializeSimplified() for facility in self.getAllFacilities()]
        statusOfPatients = [patient.serializeSimplified() for patient in self.allPatients]
        return statusOfFacilities,percentageOfInfected+f"% ({numOfInfected} out of {len(self.allPatients)})",statusOfPatients
        
    
    
    
    
    
     
    """"
        Functions for both facilites
    """      
    def getAllFacilities(self):
        return self.hospitals + self.quarantines
    
    
        
    def getFacilityById(self, id_):
        id_ = id_.strip("<>")
        theObject = self.hospitals if id_.startswith("hos") else self.quarantines
        for facility in theObject:
            if str(facility.ID) == id_:
                return facility
        return None
    
    
    def deleteFacility(self, id_):
        facilityToDel = self.getFacilityById(id_)
        id_ = id_.strip("<>")
        facilityFile = "hospitals.obj" if id_.startswith("hos") else "quarantines.obj"
        facilityType = self.hospitals if id_.startswith("hos") else self.quarantines
        if (facilityToDel != None):
            changePatientMonitored = [patient.changeAttribute("monitoredIn",None) for patient in self.allPatients if patient.monitoredIn == id_]
            facilityType.remove(facilityToDel)
            self.saveToFile(facilityFile, facilityType)
            facilityType = self.getDataFromFile(facilityFile)   
        return facilityToDel != None    
    
      
        
    def totalCapacityLeftInFacilities(self, facilityType):
        capacityLeft = 0
        for facility in facilityType:
            capacityLeft += facility.capacity - len(facility.patients)
        
        return capacityLeft
    
    
    
    
    
    
     
    """"
        Functions for saving and retrieving data from files
    """      
        
    def saveToFile(self, objFile, theObject, saveToSecondFile=None, theSecondObject=None):    
        with open(objFile,"wb") as W:
            for i in theObject:
                pickle.dump(i, W)          
        if saveToSecondFile !=None and theSecondObject != None:
            with  open(saveToSecondFile,"wb") as S:
                 for j in  theSecondObject:
                     pickle.dump(j, S)
                     
                       
    
    def getDataFromFile(self, File):
            if not path.exists(File):
                print(f"creatingNewFile {File}")
                open(File, "w")
            allA = []
            with open(File, "rb") as openfile:
                while True:
                    try:
                       allA.append(pickle.load(openfile))
                    except EOFError:
                       break       
            return allA
               