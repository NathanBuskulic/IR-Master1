# IR-Master1
In order for this project to work, you need to install elasticSearch and launch it before launching the different part of the code.

Since I cannot use the GOV2 dataset, I'm using the cran one, which is kind of crappy but it's good enough to make sure that everything work out the way it's suppose to.

I will quickly go through all the file and what they are supposed to do, then ther is a list of what is left to do.

## Files documentation :

### elasticIndexing

This file is here to create the index of the search engine and add all the document of the dataset (here Cran) to the index.

### elasticSearch

It's here that the main things happens, you will find find in that file the functions that is searching for the query in the index and rescore the results before reranking them. It also uses metrics in order to calculate the values of the search engine after sending a bunch of queries.

### myScoringFun

Here is the code for the scoring function, it uses dirichlet smoothing as well as language modelling of the query. It still need to implement all the SVM stuff.

### rerank

Here is the code of the reranking function, it takes a set of result from the index as input and uses the new scoring function to rerank the results.

### featuresCreation

The place where we calculate the features that links a query and a wikipedia page. Need some work here

### utils

A bunch of functions that are useful, kind of messy but you should find quite a lot of things in here.

### Other files

Other files are test files. I tried a bunch of stuff in them, they should not be very interesting to you.

## What need to be done

The thing here are not in an order of priority, just do what seems doable to you or more important.

### Make the dataset work

Yep it is still not working...

### Create more features for the SVM

There is a BUNCH of features that the original paper uses, I don't think we can have all of them but we can for sure rebuild some.
The features are not in the original paper but in the paper called _Learning\_Semantic\_Query\_Suggestions_ in the repository.

### Integrate the SVM to the scoring function

Yes because one we have the features we need to train the SVM and then integrate the results by expanding the query in the rescoring function. (follow the initial paper to know how to do that)

### Create the training dataset for the SVM
We need to link queries (that can be found in topics.txt) to relevant wikipedia articles in order to train the SVM. I don't know how to do that efficiently, we can maybe for now focus on a subset of the queries and make sure everything works before expanding on the entire set of queries.

### Write report
Yes because in the end that is what matters ahahah

### Benchmark
Once evrything in the code is done we need to benchmark it to include it in the reports.
