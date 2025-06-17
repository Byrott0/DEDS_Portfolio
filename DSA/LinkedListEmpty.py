from LinkedList import LinkedList
from LinkedListPopulated import LinkedListPopulated
class LinkedListEmpty(LinkedList):
     def __str__(self):
         return ""
     
     def addFirst(self, value):
         return LinkedListPopulated([value])
     
     def remove(self, value):
         return self  # Lege lijst blijft leeg, dus return zelf
     
     def smallest(self):
         raise ValueError("geen elementen in de lijst")
     
     def largest(self):
         raise ValueError("geen elementen in de lijst")
     
     def sortSimple(self):
         return self  # Lege lijst blijft leeg, dus return zelf
     
     def uniq(self):
         return 0
    