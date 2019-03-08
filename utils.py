import numpy as np
import nltk

# def languageModelingScoring(query, document, vocabulary):
#     ''' Gives the socring of the document according to the query using a language Modelling approach.
#         For now, it does not implement the query expansion using pseudo relevance feedback and wikipedia
#         in order to build the baseline.
#     '''

#     # Since the documents priors are uniform, we don't need to take it into account
#     # First get all the words of the query in lower case and without punctuation
#     querySplit =  nltk.word_tokenize(query)
#     querySplit = [word.lower() for word in querySplit if word.isalpha()]

#     # Then we get the model of the query
#     queryModel = {word : (querySplit.count(word) / len(querySplit)) for word in set(querySplit)}
#     print(queryModel)

#     # We create the same kind of model for the document
#     documentModel = documentModelSmoothed(document, vocabulary, 100)

    



# def documentModelSmoothed(document, vocabulary, mu):
#     ''' Return The language model of the document smoothed by using dirichlet smoothing.
#         Still need to apply the smoothing on the fly for words that are not in the documents.
#     '''

#     # We get all the words in the document
#     documentSplit = nltk.word_tokenize(document)
#     documentSplit = [word.lower() for word in document if word.isalpha()]

#     documentModel = {}
#     # We calculate the proba for each word
#     for word in set(documentSplit):
#         resultProba += (documentSplit.count(word) + mu * vocabulary(word)) / (len(documentSplit) + mu)
#         documentModel[word] = resultProba

#     return documentModel


def evaluationPrecision(rankingRelevance):
    ''' Return the precision of a query given the ranking of documents and the relevance judgement
        RankingRelevance is a binary list [0,1,0,0,0,1,0] of relevance judgement for each retrieved doc in the order of the original ranking.
    '''
    if len(rankingRelevance) != 0:
        return rankingRelevance.count(1) / len(rankingRelevance)
    else:
        return 0

def evaluationRecall(rankingRelevance,nbRelevantDocCorpus):
    ''' Return the recall measure
        nbRelevantDocCorpus is the number of relevant documents in the corpus.
    '''
    
    if nbRelevantDocCorpus != 0:
        return rankingRelevance.count(1) / nbRelevantDocCorpus
    else:
        return 0


def evaluationAveragePrecision(rankingRelevance, nbRelevantDocCorpus):
    ''' Return the Average precision
    '''

    result = 0
    for i in range(0,len(rankingRelevance)):
        if rankingRelevance[i] == 1:
            result += evaluationPrecision(rankingRelevance[:i])

    if nbRelevantDocCorpus != 0:
        return result / nbRelevantDocCorpus
    else:
        return 0


def evaluationMAP(listAvP):
    ''' return the MAP score over all queries in the list
    '''
    return np.mean(listAvP)


def evaluationRR(rankingRelevance):
    ''' return the RR measure
    '''

    result = 0
    if rankingRelevance.count(1) != 0:
        result = 1/(rankingRelevance.index(1) + 1)

    return result

def evaluationMRR(listRR):
    ''' Return the MRR value of the list of RR values
    '''

    return np.mean(listRR)

def getRelevanceJudgement(relevanceFile):
    ''' Get the relevance judgement from a file and format them into the format :
        {topic1 : [docRelevant1, docRelevant2], topic2 : [docRelevant1, docRelevant2]}
    '''

    result = {}
    
    flux = open(relevanceFile,'r')
    for line in flux:
        # split the line in [TOPIC, ITERATION, DOCNO, RELEVANCY]
        splitLine = line.split(' ')

        # if the document is relevant
        if int(splitLine[3][:-1]) != 0:
            # We add it to the dictionnary of relevant result
            topic = int(splitLine[0])
            docno = splitLine[2]
            if topic in result:
                result[topic].append(docno)
            else:
                result[topic] = [docno]

    flux.close()
    return result



def getTopics(topicFile):
    ''' Return the topic number associated with the title
        {topicNum : title,...}
    '''

    result = {}

    flux = open(topicFile,'r')
    fullText = flux.read()

    # we cut the text in small pieces
    indexBeginning = fullText.find("<num>")
    while indexBeginning != -1:

        # We get the topic
        fullText = fullText[indexBeginning:]
        endNumber = fullText.find('\n')
        #print(fullText[15:endNumber])
        topicNumber = int(fullText[14:endNumber])
        
        #We get the title
        beginningTitle = fullText.find("<title>")
        fullText = fullText[beginningTitle+8:]
        endTitle = fullText.find('\n')
        topicTitle = fullText[:endTitle]

        result[topicNumber] = topicTitle

        indexBeginning = fullText.find("<num>")
        
        
    return result
        

#def searchResultToRelevanceRanking(searchResult, ):
    

def getContentPilotRun(fileName):
    ''' get the content for a pilot run on the small dataset '''

    flux = open(fileName,'r')
    fullText = flux.read()

    beginningIndex = fullText.find('.I')

    result = {}

    while beginningIndex != -1:
        fullText = fullText[beginningIndex:]
        #print("LE BON DEBUT : "+fullText[:50]+"\n\n")
        #print(fullText[3:4])
        endId = fullText.find('\n')
        docID= int(fullText[3:endId])
        #print("LE DOC ID : " + str(docID))
        fullText = fullText[endId:]
        
       
        beginningContent = fullText.find(".W")
        fullText = fullText[beginningContent:]
        beginningIndex = fullText.find(".I")
        
        if beginningIndex != -1:
            #print("blabla\n\n")
            #print("FULL TEXT ::::: " + fullText[:50] + "\n\n")
            #print("beginingContent : " + str(beginningContent))
            content = fullText[3:beginningIndex]
        else:
            #print("\n WEIRDO \n")
            content = fullText[3:]

        result[docID] = content
        #print(content)

    return result


def getQueriesPilotRun(fileName):
    ''' get The queries for the pilot Run '''
    flux = open(fileName,'r')
    fullText = flux.read()

    beginningIndex = fullText.find('.I')

    result = {}

    while beginningIndex != -1:
        fullText = fullText[beginningIndex:]
        #print("LE BON DEBUT : "+fullText[:50]+"\n\n")
        #print(fullText[3:4])
        endId = fullText.find('\n')
        docID= int(fullText[3:endId])
        #print("LE DOC ID : " + str(docID))
        fullText = fullText[endId:]
        
       
        beginningContent = fullText.find(".W")
        fullText = fullText[beginningContent:]
        beginningIndex = fullText.find(".I")
        
        if beginningIndex != -1:
            #print("blabla\n\n")
            #print("FULL TEXT ::::: " + fullText[:50] + "\n\n")
            #print("beginingContent : " + str(beginningContent))
            content = fullText[3:beginningIndex]
        else:
            #print("\n WEIRDO \n")
            content = fullText[3:]

        result[docID] = content
        #print(content)

    return result


def getRelevancePilotRun(fileName):
    ''' get the relevance judgement for the pilot run '''
    flux = open(fileName,'r')
    
    result = {}
    for line in flux:
        #[Query, Doc, Relevance]
        lineSplit = line.split(" ")
        if int(lineSplit[0]) not in result:
            result[int(lineSplit[0])] = []
        #print(lineSplit)
        if int(lineSplit[2]) not in [-1,4]:
            result[int(lineSplit[0])].append(int(lineSplit[1]))
    return result


#a = getRelevancePilotRun("cran/cranqrel")
#print(a)
#a = getQueriesPilotRun("cran/cran.qry")
#print(a)
#a = getRelevanceJudgement("relev.txt")
#print(a[701])
#print(len(a[701]))
#languageModelingScoring("Je suis une une une phrase qui se phrase repete","")
    
