# FatosBerisha-COVID-19-Project
Corona Virus Infection Management System(Programming II Project)

	Documentation of Corona Virus Project

	There are 5 different classes:CovidAPI.py, CovidManagementSystem.py, Hospital.py, Quarantine.py, Staff.py and Patient.py.

	In the Hospital.py are created new hospitals which each have an id, a name, capacity, a list of patients and staff.
	These ID all start with an identifier string ("hos-....") to distinguish between hospitals and quarantines.
	The same is for quarantines except the quarantine's id starts with quar-.


	This API saves and retrieves data with the help of the package called pickle which saves the instances of classes or 
	the objects in a file in a binary format. At the beginning these files are called using the function getDataFromFile() 
	in the CovidManagementSystem class. If no file with the name given as a parameter for this file exists then this file creates 	one and then reads from it. The lists self.hospitals, quarantines, allEmployees and allPatients use this function to get the data.

- [Heading](getHospitals())

######
Functions in CovidManagementSystem.py

# hospital

## getHospitals()
  returns all hospitals from the list

## addHospital()
   creates a new Hospital and then appends that hospital to the self.hospital list, and then immediately the new data is saved in the    file "hospitals.obj"

# patient

## getPatient(patId_, facility)
   gets the patient with the given id(patId) inside the given list(facility), options are: self.hospitals, self.quarantines 
   or self.allPatients



## createNewPatient(name, dob)
creates new patient


## discharge(pat_id, facility_id)
discharges the patient with the given id(pat_id) inside the facility with the given id(facility_id)
first checks if the facility with the given id exists and then checks if the patient with the given id also exists inside this facility, if both are true then, it checks first if the patient is infected, if not then it continues with the process of discharging


## diagnose(pat_id)
finds the patient with the id(pat_id) in the list of allPatients, then simulates a test and by using the random number generator it can simulate a result, 90% of being negative to coronavirus and 10 of being positive. 
In case it is negative the patient will be discharged with the help of the previous discussed function( discharge() ).
If it is positive then the status is changed to infected and then the function transferPatientToAnyQuarantine is called.


# Related
## transferPatientToAnyQuarantine(pat_id, facilityTypeToTransfer)
finds the patient with the id(pat_id) in the list of allPatients, first checks if the patient is already in a hospital. If yes then that facility is found ,  then the patient in that facility is found and then the patient is deleted from that facility.
If the patient was in a quarantine than the function just stops because there is no need for transfering the patient in case of a positive test result.

If only the if condition or no condition at all was fulfilled than the function just transfers the patient to the first quarantine that has the capacity left to accomodate the patient.


## cure(pat_id)
same as with the diagnose fucntion with the help of the random number generator a test result will be simulated, 97% chance of the patient getting cured and 3% of not geting cured and dying.
If the result is between 97 then the patient will be discharged.
The same will happen also if the patient wasn't cured but the difference is that now the patient is labeled as dead in the system.

## admitPatientF(fac_id, pat_id)
this is used to admit a patient to any facility by giving the facility id we want to transfer the patient with id(pat_id) to.
The patient and facility will be found and if both exist and the facility with id(fac_id) has enough capacityleft, it will then check if the patient is in a facility already and if yes is that facility the same as the facility with the id(fac_id), in this case nothing will be done.
But if not then the user will be transfered to the facility with the id(fac_id).





# staff

## getEmployee(employeeId, theList)
Gets the employee with the id(employeeId) inside the given list(self.quarantines, self.hospitals or self.allEmployees)



## deleteEmployee(employeeId)
deletes the employee with the id(employeeId) from the system and from a facility in which that employee works(given that the employee works anywhere).
If the employee works anywhere:
the variable facilityFile will be created and will get the name of the file corresponding to the facility type this employee works, 
if this employee works in a quarantine than the file will be "quarantines.obj".
Same logic is with the variable facilityType which will hold the corresponding list name. These two variables will be used to determine which file and which list will need to be saved.
Then the employee is deleted from that facility and then the newchange will be saved in file that is in the variable facilityFile, 
and the data to be saved there will be taken from the list that is in the variable facilityType.



Related to staff
## saveToFile(objFile, theObject, saveToSecondFile=None, theSecondObject=None)
This function will save data to the given file(objFile), and those data will be collected from the given list(theObject). 
If it's needed than two different files and two different lists can be used by giving also the saveToSecondFile and theSecondObject.
The data will be saved using pickle.



## assignEmployee(employeeId, facilityId)
assigns an employee to the facility with the id(facilityId)
The employee will be found and if the employee already works somewhere, then the Id of that workplace will be saved in the variable formerWorkPlaceId(by getting the value of the staff attribute called "worksIn"). Then the currentWorkPlace will be found , and then inside of that facility's staff list the employee will be found and then get deleted from that facility.
Regardless if the if condition was fulfilled the new work place will be found by getting the facility with the id(facilityId).
If that facility exists than the employee will be transfered to that facility.


## addStaff(name, dob, position)
creates a new employee with the given name, dob and position(either a doctor or a nurse). These parameters will be given in the api, the position parameter there is called type.


## getAllEmployees()
gets all employees in the system


# Quarantines

## getQuarantines()
gets all the quarantines from the list self.quarantines


## addQuarantine(name, capacity)
creates a new quarantine with the given parameters

## deleteQuarantine(quarId)
deletes the quarantine with the id quarId
It finds the given quarantine, if it exists than it's patients are saved in the variable patientsOfQuar, and the number of patients.
	If the number of patients is zero than the quarantine is simply deleted.
	If not then that means that the patients of the quarantine first need to be transfered to another quarantine before being deleted.
	If the quarantine has patients:
		the function will loop inside all the quarantines, if the quarantine currently in the loop is not the same quarantine that we want to delete, then the capacity left of that quarantine will be saved.
		If the capacityLeft is 0 than the loop will continue to the other quarantine.
		If the capacityLef is greater or equal to the number of patients inside the quarantine we want to delete, then that means that we can simply just store all the patients inside this quarantine.
		patientsInAllPatients variable is used to get all the patients that are for now part of the quarantine we want to delete ,inside the list allPatients in order to later with the variable "patientsToTransferModified" change the attribute 'monitoredIn' correctly.
		And then store the patients and clear the patients list inside the quarToDelete and then call the function again recursively. And when the function starts again now the condition "if (numOfPatients == 0)" is fulfilled which means the quarantine can be safely deleted by using the function self.deleteFacility()

But if the current quarantine can't store all the patients then the next will be checked.
By using the fucntion totalCapacityLeftInFacilities() will be able to know if there is enough joint capacity in the other quarantines.
	If there is:
		Then the function stores as many patients inside the current quarantine as the quarantine allows and delete the same patients that were transfered from the list patientsOfQuar.
		And then the function is called recursively to check if all patients were transfered, if not go again into the for loop and repeat the same steps


If none of the conditions inside the for loop were met than that means that the patients can't be transfered thus the quarantine can't be deleted.		



## capacityLeftOfAllQuaranatines()
gets the joint capacityLeft of all quarantines



# stats

## systemStats()
calculates the number and percentage of the infected patients, gets the status and id-s of all facilities, and the status and ID-s of all patients


# both facilities
these functions will be used for the hospital and quarantine functions

## getAllFacilities()
gets all facilities by joining the lists :self.hospitals and self.quarantines

## getFacilityById(id_)
gets the facility with id(id_)
It determines whether the given id_ is that of a hospital or a quarantine by checking if the id_ startswith("hos") or with "quar".
And then it starts looking in the list of hospitals or quarantines


## deleteFacility(id_)
deletes the facility with id_
if the facility with that id exists first changes the patients attribute called 'monitoredIn' to null since those patients will still show up in the allPatients list even after deletion of their facility.





# saving and retrieving data


## getDataFromFile(File)
get data from the given file, if that file doesn't exist createIt

## saveToFile(objFile, theObject, saveToSecondFile=None,  theSecondObject=None)
This function will save data to the given file(objFile), and those data will be collected from the given list(theObject). If it's needed than two different files and two different lists can be used by giving also the saveToSecondFile and theSecondObject.
The data will be saved using pickle.
