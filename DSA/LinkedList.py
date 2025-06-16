from abc import ABC, abstractmethod
import csv
import sys

class LinkedList(ABC):

    @abstractmethod
    def __str__(self): pass

    @abstractmethod
    def addFirst(self, value): pass

    @abstractmethod
    def remove(self, value): pass

    @abstractmethod
    def smallest(self): pass

    @abstractmethod
    def largest(self): pass

    @abstractmethod
    def sortSimple(self): pass