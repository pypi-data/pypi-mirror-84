import feedparser

def setup():
    entries = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')['entries']
    list = []
    for i in range(len(entries)):
        list.append(entries[i])
    return(list)

def title():
    list = []
    set = setup()
    for i in range (len(set)):
        list.append((set[i]['title']))
    return(list)

def description():
    list = []
    set = setup()
    for i in range (len(set)):
        list.append((set[i]['summary']))
    return(list)

def link():
    set = setup()
    list = []
    for i in range (len(set)):
        list.append((set[i]['links'][0]['href']))
    return(list)
