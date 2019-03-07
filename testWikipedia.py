import wikipedia as wkp

search = wkp.search("barack obama",results=100)
print(search)

barack = wkp.page(search[0])
print(barack.content)
