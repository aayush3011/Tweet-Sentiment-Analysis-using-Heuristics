import sys
import csv


# this function returns a dictionary of the sent scores for each term given in the AFINN-111.txt file.
# term is the key of the dictionary with its sent score as a value.
def sent_file(file):
    scores = {}
    for line in file:
        term, score = line.split("\t")
        scores[term] = float(score)
    return scores


# this function returns a dictionary of the breaking bad actors as a key with the value being a list of their tweets.
def actor_tweet_dict(file_break_bad_actor):
    actor_tweet_sentiment = {}
    for row in file_break_bad_actor:
        username = row[0]
        if username in actor_tweet_sentiment.keys():
            actor_tweet_sentiment[username].append(row[1])
        else:
            actor_tweet_sentiment[username] = []
            actor_tweet_sentiment[username].append(row[1])
    return actor_tweet_sentiment


# thi function calculates the average sentiment score for tweets of the breaking bad actors.
def happiest_actor(file_sent, file_break_bad_actor):
    actor_tweets = actor_tweet_dict(file_break_bad_actor)
    sent = sent_file(file_sent)
    happiest_actor_scores = {}
    for name in actor_tweets:
        tweets_len = len(actor_tweets[name])
        sent_score_tweet = 0

        for tweet in actor_tweets[name]:
            terms_in_line = [term for term in tweet.replace("\n", " ").lower().split(" ")]
            for term in terms_in_line:
                if term in sent:
                    sent_score_tweet += sent[term]
                else:
                    sent_score_tweet += 0
        avg_sent_score = sent_score_tweet/tweets_len
        happiest_actor_scores[name] = avg_sent_score
    return happiest_actor_scores


# this function print the happiest actors in descending as score: username.
def print_happiest_actor(file_sent, file_tweet):
    happiest_actor_scores = happiest_actor(file_sent, file_tweet)
    for w in sorted(happiest_actor_scores, key=happiest_actor_scores.get,reverse=True):
        print("% .4f" % happiest_actor_scores[w]+":", w)


def main():
    sentiment_file = open(sys.argv[1])
    csv_file = open(sys.argv[2])
    file_reader = csv.reader(csv_file)
    next(file_reader, None)
    print_happiest_actor(sentiment_file, file_reader)

    #TODO: Implement

if __name__ == '__main__':
    main()
