import oauth2
import urllib.parse
import json

class Twtlib:
    def __init__(self, api_key, api_secret, token_key, token_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_key = token_key
        self.token_secret = token_secret

        consumer = oauth2.Consumer(self.api_key, self.api_secret)
        token = oauth2.Token(self.token_key, self.token_secret)
        self.client = oauth2.Client(consumer, token)

    def buscar(self, query, lang):
        query_codificada = urllib.parse.quote(query, safe='')
        req = self.client.request(
            'https://api.twitter.com/1.1/search/tweets.json?q=' + query_codificada + '&lang=' + lang)
        decode = req[1].decode()
        resp = json.loads(decode)
        tweets = resp['statuses']
        for tweet in tweets:
            print('<User>: ', tweet['user']['screen_name'])
            print('<Text>: ', tweet['text'])
            print("")
            print('-------------------------------------------------------------------------------------')

    def postar(self, post):
        try:
            query_codificada = urllib.parse.quote(post, safe='')
            req = self.client.request('https://api.twitter.com/1.1/statuses/update.json?status=' + query_codificada,
                                      method='POST')
            decode = req[1].decode()
            resp = json.loads(decode)
            print("Success! ")
        except:
            print("Error. ")
