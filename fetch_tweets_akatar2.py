import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import sys
import csv

# See Assignment 1 instructions for how to get these credentials
access_token_key = "2714571763-qi5sAVQk8RYSC3YWsriiuSUht0uBYSnEc5ySEw8"
access_token_secret = "6RrXqZ9OfsZsHDJXmHfiflCmaPgL9wZcxrfzdFIZ0EUZw"

consumer_key = "OlBD4WpItuK8jxXkFO5n5fLr6"
consumer_secret = "Jvobja4fDLh6XJGYFFcYbKiU13zjjupnXmoOBtp9iuo1CQqiQN"

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''


def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetch_samples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        print(line.decode('utf-8').strip())


def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term), ("count", "100")]
    response = twitterreq(url, "GET", parameters)
    print(response.readline())


def fetch_by_user_names(user_name_file):
    # TODO: Fetch the tweets by the list of usernames and write them to stdout in the CSV format
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    f = open(user_name_file)
    screen_names = f.read()
    f.close()
    user_name_list = screen_names.split("\n")
    names_dict = {}
    for stars in user_name_list:
        stars = stars.strip()
        if stars:
            parameters = [("screen_name", stars), ("count", "100")]
            response = twitterreq(url, "GET", parameters)
            tweets = json.loads(response.read().decode('utf-8'))
            names_dict[stars] = []
            if response.status == 200:
                for line in tweets:
                    # print(line['text'].encode('utf-8'))
                    names_dict[stars].append(line['text'].encode('utf-8'))
    writer = csv.writer(sys.stdout)
    header = ['user_names', 'tweet']
    writer.writerow(header)
    for user_name in names_dict:
        for tweet in names_dict[user_name]:
            writer.writerow([user_name, tweet])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True, help='Enter the command')
    parser.add_argument('-term', help='Enter the search term')
    parser.add_argument('-file', help='Enter the user name file')
    opts = parser.parse_args()
    if opts.c == "fetch_samples":
        fetch_samples()
    elif opts.c == "fetch_by_terms":
        term = opts.term
        print(term)
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
