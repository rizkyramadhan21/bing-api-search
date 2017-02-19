import urllib
import urllib2
import json
import sys

def main():
    import sys
    key = 'Your Bing API Key'
    if len(sys.argv)>1:
        key = sys.argv[1]
    if not key:
        print ">> Please Input your Bing API Keys <<"
        return 0
    bing = Bing(key)
    result = bing.search("kata kunci pencarian")
    if result:
        for el in result:
            print "[%s](%s)" % (el.get('Title','no title'),
                    #el.get('Description','no description'),
                    el.get('Url','no url'))
    else:
        print "_Hasil tidak ditemukan_ :("

class Bing:
    key = ''

    def __init__(self,key,top=6,search_type="Web"):
        # Custom parameters for this instance
        # This could be overrided in every search
        self.key = key
        self.top = top
        self.search_type = search_type

    def search(self, query, **kwargs):
        key=self.key
        query = urllib.quote(query)
        top = kwargs.get("top",self.top)
        search_type = kwargs.get("search_type",self.search_type)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'

        # prepare the credentials
        credentials = (':%s' % key).encode('base64')[:-1]
        auth = 'Basic %s' % credentials

        # generate query url
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type
        url+='?Query=%27'+query+'%27'
        url+='&$top='+str(top)+'&$format=json'

        # query BING
        request = urllib2.Request(url)
        request.add_header('Authorization', auth)
        request.add_header('User-Agent', user_agent)
        request_opener = urllib2.build_opener()
        try:
            response = request_opener.open(request)
            response_data = response.read()
            json_result = json.loads(response_data)
            result_list = json_result['d']['results']
        except urllib2.HTTPError as error:
            raise

        # array hasil pencarian
        return result_list

if __name__ == "__main__":
    main()
