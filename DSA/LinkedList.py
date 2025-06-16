
from abc import ABC, abstractmethod

class LinkedList(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        if not self:
            return ""
        # als de linked list leeg is, return een lege string
        if len(self) == 1:
            return str(self[0])
        # als de linked list meer dan 1 element heeft, return eerste element plus rest
        return str(self[0]) + " " + str(self[1:])
    
    # Test 1: Lege lijst
print("[" + str([]) + "]")     # Verwacht: []

# Test 2: Lijst met 1 element
print("[" + str([5]) + "]")    # Verwacht: [5 ]

# Test 3: Lijst met 2 elementenF
print("[" + str([4, 7]) + "]") # Verwacht: [4 7 ]

def addFirst(value, self):
    return [value] + self

print ("addfirst methode test")
# Test 1: Lege lijst
print(addFirst(5, []))            # Verwacht: [5]

# Test 2: Lijst met 1 element
print(addFirst(5, [4]))           # Verwacht: [5, 4]

# Test 3: Lijst met meerdere elementen
print(addFirst(5, [4, 7]))        # Verwacht: [5, 4, 7]

# Test 4: Lijst met strings
print(addFirst("a", ["b", "c"]))  # Verwacht: ["a", "b", "c"]


def remove(value, lst):
    if not lst:
        return []
    if lst[0] == value:
        return lst[1:]  # sla de eerste match over en return de rest
    return [lst[0]] + remove(value, lst[1:])

def smallest(self):
    if len(self) == 1:
        return self[0]
    return min(self[0], smallest(self[1:]))
print(smallest([5, 4, 3,2, 7]))  # Output: 3

#class LinkedListPopulated:

#class LinkedListEmpty:

