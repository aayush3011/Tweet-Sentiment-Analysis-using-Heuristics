import sys
import json


# this function returns a dictionary of the sent scores for each term given in the AFINN-111.txt file.
# term is the key of the dictionary with its sent score as a value.
def sent_scores(file_sent):
    scores = {}
    for line in file_sent:
        term, score = line.split("\t")
        scores[term] = float(score)
    return scores


# this function creates a dictionary of the US states with their abbreviations as the values.
def state_abbrv():
    abbrv = {"Alabama": "AL", "Alaska": "AK",  "Arizona": "AZ",  "Arkansas": "AR",  "California": "CA", "Colorado": "CO",
            "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
            "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
            "Kentucky": " Ky", "Louisiana": "LA", "Maine": "ME", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
            "New Hampshire": "NH", "New Jersey": "NJ","New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
            "North Dakota": "ND", "Ohio": 'OH', "Oklahoma": "OK","Oregon": "OR", "Maryland": "MD", "Massachusetts": "MA",
            "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS","Missouri": "MO", "Pennsylvania": "PA",
            "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
            "Utah": "UT", "Vermont": "VI", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
            "Wyoming": "WY"}
    return abbrv


# this function returns a dictionary with the abbreviation of the state of the tweet as a key and the tweets from these
# states as a list of values of the dictionary.
def state_tweet(file_tweet):
    state_tweets = {}
    state_abbs_dict = state_abbrv()
    for line in file_tweet:
        tweets = json.loads(line)
        if tweets['place'] is not None:
            if tweets['place']['country'] == "United States":
                if tweets['place']['place_type'] == "city":
                    state_abbr = tweets['place']['full_name'].split(",")[1].strip()
                    if state_abbr in state_tweets:
                        state_tweets[state_abbr].append(tweets['text'])
                    else:
                        state_tweets[state_abbr] = []
                        state_tweets[state_abbr].append(tweets['text'])
                elif tweets['place']['place_type'] == "admin":
                    state_abbr = state_abbs_dict[tweets['place']['full_name'].split(",")[0].strip()]
                    if state_abbr in state_tweets:
                        state_tweets[state_abbr].append(tweets['text'])
                    else:
                        state_tweets[state_abbr] = []
                        state_tweets[state_abbr].append(tweets['text'])
                else:
                    continue
            else:
                continue
        else:
            continue
    return state_tweets


# this function returns the happiest states by calculating the average sent score of the tweets from each state.
def happy_states_sent(file_sent, file_tweet):
    happy_state = {}
    sent = sent_scores(file_sent)
    state_tweets = state_tweet(file_tweet)

    for state in state_tweets:
        tweets_len = len(state_tweets[state])
        sent_score_tweet = 0

        for tweets in state_tweets[state]:
            term_in_line = [term for term in tweets.replace("\n", " ").lower().split(" ")]
            for term in term_in_line:
                if term in sent:
                    sent_score_tweet += sent[term]
                else:
                    sent_score_tweet += 0
        happy_state[state] = sent_score_tweet/tweets_len
    return happy_state


# this function prints the top 5 happiest states with their sentiment scores.
def print_happy_states(file_sent, file_tweet):
    happiest_states = happy_states_sent(file_sent, file_tweet)
    for state in sorted(happiest_states, key=happiest_states.get, reverse=True):
        print("%.4f" % happiest_states[state]+":", state)


# this function prints the top 5 unhappiest states with their sentiment scores.
def print_unhappy_states(file_sent, file_tweet):
    happiest_states = happy_states_sent(file_sent, file_tweet)
    for state in sorted(happiest_states, key=happiest_states.get, reverse=False)[0:5]:
        print("%.4f" % happiest_states[state]+":", state)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #print_happy_states(sent_file, tweet_file)
    print_unhappy_states(sent_file, tweet_file)
    #TODO: Implement

if __name__ == '__main__':
    main()
