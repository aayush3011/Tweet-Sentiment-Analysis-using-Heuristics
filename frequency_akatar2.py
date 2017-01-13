import sys
import json


# this function returns a list of the stop words given in the stopwords.txt file.
def stop(file_1):
    stop_words = file_1.read()
    stop_words_list = stop_words.split("\n")
    return stop_words_list


# this function takes two arguments one the stopwords file and other the tweet file.
# it counts the term in each tweet except the stopwords and counts the term frequency of all the terms.
def tweet_freq(file_1, file_2):
    count_all = {}
    count_all_terms = 0
    stop_word_list = stop(file_1)
    for line in file_2:
        tweets = json.loads(line)
        terms_in_line = [term for term in tweets['text'].lower().split(" ") if
                         term not in stop_word_list]
        count_all_terms += len(terms_in_line)

        for single_term in terms_in_line:
            if single_term not in count_all:
                count_all[single_term] = 1
            else:
                count_all[single_term] += 1

    for term in count_all:
        count_all[term] = count_all[term] / count_all_terms
    # print(count_all)
    return count_all


# this function prints the solution as the term with its term frequency.
def print_frequency(file_1, file_2):
    term_freq = tweet_freq(file_1, file_2)
    for w in sorted(term_freq, key=term_freq.get, reverse=True)[0:30]:
        print(w, term_freq[w])


def main():
    stop_words_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    print_frequency(stop_words_file, tweet_file)
    # TODO: Implement


if __name__ == '__main__':
    main()
