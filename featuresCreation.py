import numpy as np


def find_all(bigStr,substr):
    ''' return all the occurences of a substring in a string'''
    start = 0
    result = []
    index = bigStr.find(substr)
    while index != -1:
        result.append(index)
        start = index + len(substr)
        index = bigStr.find(substr,start)
    return result
    

print(find_all("test test test test","test"))

# We assume we have the wikipedia page in a nice string format
def TF(query, wkpage):
    return len(find_all(wkpage,query)) / len(wkpage)

def SPR(query,wkpage):
    allOcc = find_all(wkpage,query)
    print(allOcc)
    return allOcc[len(allOcc) - 1] - allOcc[0]

def allPos(query, wkpage):
    allOcc = find_all(wkpage,query)
    return [i/len(wkpage) for i in allOcc]

def QCT(query,wkage):
    return wkpage.fin

wkpage = "test test test testtest"
query = "test"
print(SPR(query,wkpage))
