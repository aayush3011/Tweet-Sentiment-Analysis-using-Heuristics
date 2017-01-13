import sys
import json


# this function returns a dictionary of the sent scores for each term given in the AFINN-111.txt file.
# term is the key of the dictionary with its sent score as a value.
def sent_scores(file):
    scores = {}
    for line in file:
        term, score = line.split("\t")
        scores[term] = float(score)
    return scores


# this function takes two arguments one the sentiment file and other the tweet file.
# it calculates the sentiment score for each tweet in the streaming_output_full.txt file.
def tweet_sent(file_sent, file_tweet):
    tweet_sentiment = {}

    sent = sent_scores(file_sent)
    for line in file_tweet:
        tweets = json.loads(line)
        sent_score_text = 0
        terms_in_line = [term for term in tweets['text'].replace("\n", " ").lower().split(" ")]
        for term in terms_in_line:
            if term in sent:
                sent_score_text += sent[term]
            else:
                sent_score_text += 0
        tweet_sentiment[tweets['text'].replace("\n", " ")] = sent_score_text
    return tweet_sentiment


# this function prints the top 10 highest sentiment score tweets in descending as the score for each tweet followed
# with the actual tweet.
def print_tweet_sentiment_highest(file_sent, file_tweet):
    tweet_sentiment = tweet_sent(file_sent, file_tweet)
    for tweet in sorted(tweet_sentiment, key=tweet_sentiment.get, reverse=True)[0:10]:
        print("% .4f" % tweet_sentiment[tweet]+":" , tweet)


# this function prints the top 10 lowest sentiment score tweets in descending as the score for each tweet followed
# with the actual tweet.
def print_tweet_sentiment_lowest(file_sent, file_tweet):
    tweet_sentiment = tweet_sent(file_sent, file_tweet)
    for tweet in sorted(tweet_sentiment, key=tweet_sentiment.get, reverse=False)[0:10]:
        print("% .4f" % tweet_sentiment[tweet]+":", tweet)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #print("The top 10 highest sentiment tweets:")
    #print_tweet_sentiment_highest(sent_file, tweet_file)
    print("The top 10 lowest sentiment tweets:")
    print_tweet_sentiment_lowest(sent_file, tweet_file)
    #TODO: Implement

if __name__ == '__main__':
    main()
