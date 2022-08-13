'''
Class that creates the Item object
Only used so that users don't have to use json 
'''

class Item:
   def __init__(self, id, serial, rap, value):
     self.id = id
     self.serial = serial
     self.rap = rap
     self.value = value
