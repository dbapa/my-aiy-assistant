import json
import urllib.request
import my_locker as locker

class DBNewsReader:
    
    NEWS_URL = 'https://newsapi.org/v1/articles'
    
    newsSources = {'BBC':'bbc-news', 'Business insider': 'business-insider', 'Al Jazeera': 'al-jazeera-english', 
                  'The Hindu': 'the-hindu', 'The Washington Post': 'the-washington-post'}
    
    def __init__(self):
        self.sampleData = [] # this may not be required
    
    # returns a list of news sources
    def get_news_sources(self):               
        srcs=[]        
        for key, val in self.newsSources.items() :
            srcs.append(key)            
        return srcs
    
    def get_news_sources_as_text(self):
        srcs = self.get_news_sources()
        srcList = ''
        print ('no of sources is %d' % len(srcs))
        for x in range(len(srcs)):
            srcList += srcs[x] + ' ; '
        return srcList
    
    # return a dictionary of news titles and descriptions
    def get_news(self, source):
        newsDictionary = {}
        #print ('getting news from :',source)
        key = source
        val = self.newsSources[key]
        url  = self.compile_top_news_url(val)
        #print ('requesting data from %s' % url)        
        req = urllib.request.Request(url)
        result = {}
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            #print ('data with length :', len(data))
            result = json.loads(data)
        '''
        f = open('/home/pi/sample_newsfeed.txt','r')
        results = f.read()
        print ('Raw results:\n',results)
        result = json.loads(results)
        f.close()                
        print ('Json result:\n',result)
        print ('type of result is:',type(result))        
        '''
        if result['status'] != 'ok' :
            return {'error': 'result page did not respond correctly'}
        
        articles = result['articles']
        
        for i in range(len(articles)) :
            article = articles[i]
            t = 'News # ' + str(i+1)+ ' : '+ str(article['title'])
            newsDictionary[t] = str(article['description'])
        #print ('No of articles:',len(newsDictionary))
        return newsDictionary
        
    def compile_top_news_url(self, source):
        key = locker.getContent("newsapi.org","key")
        url = self.NEWS_URL + '?source=' + source + '&sortBy=Top&apiKey=' + key
        return url
       
def main():
    c = DBNewsReader()
    src = c.get_news_sources_as_text()
    print (src)
    newsD  = c.get_news('BBC')
    for key, val in newsD.items() :
        print('Title:\n', key)
        print('news:\n',val)

if __name__ == '__main__' :
    main()