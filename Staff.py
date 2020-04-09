# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:41:47 2020

@author: Fatos
"""
import uuid
class Staff:
    def __init__(self, name, dob, position):
        self.ID = str(uuid.uuid1())
        self.name = name
        self.dob = dob
        self.position = position
        self.worksIn = None
        
       
        
        
    def changeAttribute(self, attribute, newVal):
        if attribute == "position":
            self.position = newVal
        elif attribute == "worksIn":
            self.worksIn = newVal
    



        
    def serialize(self):
         return {
             "id":self.ID,
             "name":self.name,
             "dob":self.dob,
             "position":self.position,
             "Place Of Work":self.worksIn
                
             }
     

