from WebPage import WebPageIndex  # Importing WebPageIndex class
from WebPage import WebpagePriorityQueue  # Importing WebpagePriorityQueue class
import os  # Importing os for os.listdir


def readFiles(folder):
    """Takes folder path as input and returns
    a list of WepPageIndex instances."""
    instances = [] # list of instances
    for filename in os.listdir(folder):  # Checks each file in folder
        if filename == ".DS_Store":
            pass
        else:
            WebIndex = WebPageIndex(filename)  # Creates instances
            instances.append(WebIndex)  # Adds to list of instances

    return instances


def main(file):
    """ Given query file, processes each query
    with set of instances and files that match."""
    f = open(file, 'r')
    line = f.readline()
    instances = readFiles("")  # Insert folder path in  " "
    num = 0
    w = object
    while line != "" and line != "\n":
        print()
        print()
        print()
        if num == 0:
            w = WebpagePriorityQueue(line, instances)  # Checks first query
            print(line)
            w.printHeap()  # Printing  matching files

        else:
            w.reheap(line)  # Reheaping after each new query
            print(line)
            w.printHeap()

        line = f.readline()
        num += 1


if __name__ ==  "__main__":
    main("queries.txt")  # Insert query file name in " "
