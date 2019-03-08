import sys
import numpy as np
import wikipedia as wkp
from utils import getTopics

#get all queries :
myTopics = getTopics("topics.txt")

# start to write the file
flux = open("queryToWk.txt","w")
flux.write("")
flux.close()

for i in myTopics:
    query = myTopics[i]
    print("\n \n \n" + query + "\n")
    # print the wkp search
    classWk = wkp.search(query)
    classWithScore = []
    for j in range(len(classWk)):
        classWithScore.append((classWk[j],j))
    print(classWithScore)

    # Ask the user which one is relevant
    relevant = input("Which ones are relevant ? (numbers with space in between)\n")
    relevant = relevant.split(" ")
    #if len(relevant) > 0 and relevant[0] != '':
    relevant = [int(i) for i in relevant if i != '']

        # We add the answer to the file
        
    stringToAdd = str(i)
    for r in relevant:
        stringToAdd += " " + str(r)
    #else:

    flux = open("queryToWk.txt", 'a+')
    flux.write(stringToAdd + "\n")
    flux.close()


