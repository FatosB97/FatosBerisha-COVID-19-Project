from flask import Flask, request, jsonify
from CovidManagementSystem import *
from Hospital import * 
from Quarantine import *

app = Flask(__name__)

# Root object for the management system
ms = CovidManagementSystem ()


"""
Hospital
"""
#Add a new hospital (parameters: name, capacity). 
@app.route("/hospital", methods=["POST"])
def addHospital():
    name = request.args.get("name")
    capacity = request.args.get("capacity")
    checkValidity = [name, capacity]
    if all(var != None and var != "" for var in checkValidity):
       result = ms.addHospital(name, capacity)

    else:
        result = False,f"Not valid parameters or no parameters given!"
    return jsonify(success = result[0],
                   message = result[1])




#Return the details of a hospital of the given hospital_id. 
@app.route("/hospital/<hospital_id>", methods=["GET"])
def hospitalInfo(hospital_id):       
    h = ms.getFacilityById(hospital_id)
    if(h!=None): 
        return jsonify(h.serializeExtended())
    return jsonify(
            success = False,
            message = "Hospital not found")




# Admission of a patient to a given hospital 
@app.route("/hospital/<hospital_id>/patient", methods=["POST"])
def admitpatient(hospital_id):
    h = ms.getFacilityById(hospital_id)
    if(h!=None and float(h.occupancy()) <= 100.0):
        name = request.args.get("name")
        dob =  request.args.get("dob")
        checkValidity = [name, dob]
        if all(var != None and var != "" for var in checkValidity):
            addPatient = h.admission(name, dob)
            ms.allPatients.append(addPatient)
            ms.saveToFile("hospitals.obj", ms.hospitals, saveToSecondFile="patients.obj", theSecondObject=ms.allPatients)
            result = True,f"Patient with name:{name} with date of birth: {dob} was added to the hospital with id{hospital_id}" 
        else:
            result = False, f"Not valid or no parameters were given"
            
    elif(h!=None and float(h.occupancy()) >= 100.0):
        result = False, f"Hospital with id:{hospital_id} has not enough capacity left to add the patient!"
    else:
        result = False, f"Hospital with id:{hospital_id} not found!"
        
    return jsonify(
            success = result[0], 
            message = result[1])     
 
    


@app.route("/hospital/<hospital_id>", methods=["DELETE"])
def deleteHospital(hospital_id):
    if hospital_id.strip("<>").startswith("hos"):
        result = ms.deleteFacility(hospital_id)   
        if(result): 
            message = f"Hospital with id{hospital_id} was deleted" 
        else: 
            message = "Hospital not found" 
    else:
        message = "The given ID is not a valid hospital id!"
        
    return jsonify(
            success = result, 
            message = message)



@app.route("/hospitals", methods=["GET"])
def allHospitals():   
    hospitals = ms.getHospitals()
    return jsonify(hospitals=[x.serialize() for x in hospitals])



"""
Quarantine
"""
@app.route("/quarantine", methods = ["POST"])
def addQuarantine():
    name = request.args.get("name")
    capacity = request.args.get("capacity")
    checkValidity = [name, capacity]
    if all(var != None and var != "" for var in checkValidity):
       result = ms.addQuarantine(name, capacity)
    else:
        result = False,f"Not valid parameters or no parameters given!"
    return jsonify(success = result[0],
                   message = result[1])


@app.route("/quarantine/<quarantine_id>", methods=["GET"])
def quarantineInfo(quarantine_id):       
    q = ms.getFacilityById(quarantine_id)
    if(q!=None): 
        return jsonify(q.serializeExtended())
    return jsonify(
            success = False,
            message = "Quarantine not found")



@app.route("/quarantine/<quarantine_id>", methods=["DELETE"])
def deleteQuarantine(quarantine_id):
    result = ms.deleteQuarantine(quarantine_id)
    return jsonify(
            success = result[0], 
            message = result[1])



@app.route("/quarantine/<qu_id>/<pat_id>", methods=["POST"])
def admitpatientQuarantine(qu_id, pat_id):
    qu_id = qu_id.strip("<>")
    if qu_id.startswith("quar"):
        result = ms.admitPatientF(qu_id, pat_id)
    else:
        result = False,f"{qu_id} is not a valid quarantine id!"
    return jsonify( success=result[0],
                   message=result[1])



@app.route("/quarantines", methods=["GET"])
def allQuarantines():
    return jsonify(quarantines = [x.serialize() for x in ms.getQuarantines()])




"""
Staff
"""
@app.route("/staff", methods=["POST"])
def newEmployee():
    name = request.args.get("name")
    dob = request.args.get("dob")
    position = request.args.get("type")
    checkValidity = [name, dob , position]
    if all(var != None and var != "" for var in checkValidity):
        position = position.casefold()
        if position != "doctor" and position != "nurse":
            return jsonify(f"Type:{position} is not valid position for a staff member!")
        result = ms.addStaff(name, dob, position)
        
    else:
        result = False, f"Not valid parameters or no parameters given!"
    return jsonify(success = result[0],
                   message = result[1])




@app.route("/staff", methods=["GET"])
def allEmployees():
    staff = ms.getAllEmployees()
    return jsonify(Staff=[employee.serialize() for employee in staff])





@app.route("/staff/<staff_id>", methods=["DELETE"])
def deleteEmployee(staff_id):
   result = ms.deleteEmployee(staff_id)
   return jsonify(success = result[0],
                  message = result[1])




  
    

@app.route("/staff/<staff_id>", methods=["PUT"])
def assignEmp(staff_id):
    workPlace = request.args.get("workplace")
    if (workPlace != None and workPlace != ""):
        result = ms.assignEmployee(staff_id,workPlace)
    else:
        result = False, "Not valid or no parameters were given!"
    return jsonify(success = result[0],
                   message = result[1])    
    




"""
Patient
"""


@app.route("/patient", methods=["POST"])
def addPatient():
    name = request.args.get("name")
    dob = request.args.get("dob")
    checkValidity = [name,dob]
    if all(var != None and var != "" for var in checkValidity):
        result = ms.createNewPatient(name, dob)
    else:
        result = False, "Not valid parameters or no parameters given"
    return jsonify(
                 success = result[0],
                 message = result[1]
        )





@app.route("/patients", methods=["GET"])
def getPatients():
    allP = ms.allPatients
    return jsonify(patients=[patient.serialize() for patient in allP])





@app.route("/patient/<pat_id>/admit/<facility_id>", methods=["PUT"])
def admitPatient(pat_id, facility_id):
    result = ms.admitPatientF(facility_id, pat_id)
    return jsonify(
            success = result[0],
            message = result[1]
        )




    
@app.route("/patient/<pat_id>/discharge/<facility_id>", methods=["PUT"])
def dischargePatient(pat_id, facility_id):
    result = ms.discharge(pat_id, facility_id)
    return jsonify( result = result[0],
                    message=result[1])



@app.route("/patient/<pat_id>/diagnosis", methods=["POST"])
def diagnosePatient(pat_id):
    result = ms.diagnose(pat_id)
    return jsonify(
        result= result[0],
        message=result[1]
        )




@app.route("/patient/<pat_id>/cure", methods=["POST"])
def curePatient(pat_id):
    result = ms.cure(pat_id)
    return jsonify(
        result = result[0],
        message = result[1]
        )



"""
Stats
"""

@app.route("/stats", methods = ["GET"])
def stats():
    theStats = ms.systemStats()
    statsOfFac = {"Status of all facilities":theStats[0],"Percentage of all infected patients":theStats[1],"Information of all patients":theStats[2] }
    return jsonify (statsOfFac)





@app.route("/")
def index():
    return jsonify(
            success = True,
            message = "Your server is running! Welcome to the Covid API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=False, port=8888)
