# IR-Master1
In order for this project to work, you need to install elasticSearch and launch it before launching the different part of the code.

I will quickly go through all the file and what they are supposed to do, then ther is a list of what is left to do.

## Files documentation :

### elasticIndexing

This file is here to create the index of the search engine and add all the document of the dataset to the index.

### elasticSearch

It's here that the main things happens, you will find find in that file the functions that is searching for the query in the index and rescore the results before reranking them. It also uses metrics in order to calculate the values of the search engine after sending queries.

### myScoringFun

Here is the code for the scoring function, it uses dirichlet smoothing as well as language modelling of the query.

### rerank

Here is the code of the reranking function, it takes a set of result from the index as input and uses the new scoring function to rerank the results.

### featuresCreation

The place where we calculate the features that links a query and a wikipedia page.

### utils

A bunch of functions that are useful.

