# -*- coding: utf-8 -*-
import glob, csv, MeCab

def make_tweet_list(file):
    reader = csv.reader(file)
    tweet_list = []
    for row in reader:
        tweet_list.append(row[5])
    return tweet_list

def make_word_list(tweet_list):
    ignore_list = ['BOS/EOS',
                   '記号',
                   '数',
                   '助詞',
                   '助動詞',
                   '接頭',
                   '接尾',
                   '特殊',
                   '非自立']
    word_list = []
    for tweet in tweet_list:
        tagger = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        text = tweet.replace('　', ' ')
        node = tagger.parseToNode(text)
        while node:
            feature = node.feature.split(',')
            if (not '@' in node.surface and
                not feature[-3] == '*' and
                not any(ignore in feature for ignore in ignore_list)):
                word_list.append((feature[-3].decode('utf-8'),
                                  feature[0].decode('utf-8')))
            node = node.next
    return word_list

def count_words(word_list):
    counted_list = []
    result = []
    for word in word_list:
        if word in counted_list:
            continue
        result.append((word, word_list.count(word)))
        counted_list.append(word)
    result.sort(key=lambda p:p[1], reverse=True)
    return result

if __name__ == '__main__':
    file_names = glob.glob('data/*.csv')
    word_list = []
    for name in file_names:
        print name
        datafile = open(name)
        word_list.extend(make_word_list(make_tweet_list(datafile)))
    result = count_words(word_list)
    for i in range(101):
        print i, result[i][0][0], result[i][0][1], result[i][1]