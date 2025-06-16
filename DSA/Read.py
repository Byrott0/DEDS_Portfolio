import csv
import os
import sys

sys.setrecursionlimit(20000000)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from LinkedList import LinkedList
from LinkedListPopulated import LinkedListPopulated
from LinkedListEmpty import LinkedListEmpty

kentekens = LinkedListEmpty()

with open(sys.argv[1]) as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        kentekens = kentekens.sortSimple(row[0])