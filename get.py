import requests

#trys to get the url 5 times, uses a user-agent that looks like a standard browser
def get(url, attempts = 5):
    for i in xrange(1, attempts + 1):
        try:
            return requests.get(url,
                                headers = {
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                                    },
                                timeout = 20)
        except requests.ConnectionError:
            error = "Connection error"
        except requests.exceptions.Timeout:
            error = "Timeout exception"
        except Exception as err:
            error = "Weird error: " + str(err)
        print "{2}, retrying ({0}/{1})".format(i, attempts, error)    
    raise Exception("Request is fricked")
