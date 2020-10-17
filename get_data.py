# python3 script to scrape the data for the star wars vs harry potter movie classifier

import requests
import bs4 as bs

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import re
import pandas as pd 

stopwords = set(stopwrds.words('english'))

url_start = 'https://www.imdb.com/scripts/'
url_end = '.html'
# example url = https://www.imsdb.com/scripts/Star-Wars-Return-of-the-Jedi.html


star_wars_movies = ['Star Wars A New Hope',
                    'Star Wars Attack of the Clones', 
                    'Star Wars Return of the Jedi',
                    'Star Wars Revenge of the Sith', 
                    'Star Wars the Empire Strikes Back', 
                    'Star Wars the Force Awakens', 
                    'Star Wars the Phantom Menace', ]




def get_star_wars_script(movie_name):
	# returns the script as list of words after removing 
	# stopwords and other unnecessaary symbols and numbers
    movie_name = movie_name.replace(' ', '-')
    url = url_start + movie_name + url_end
    page = requests.get(url).text
    soup = bs.BeautifulSoup(page, 'lxml')
    script = soup.find('td', class_='scrtext').text
    script = re.sub(r'[^a-zA-Z]', ' ', script)
    script = word_tokenize(script)
    filtered_script = [w.lower() for w in script if w not in stop_words]
    return filtered_script

def get_potter_script(chapter):
    # example url https://www.hogwartsishere.com/library/book/7391/chapter/4/
    url = 'https://www.hogwartsishere.com/library/book/7391/chapter/' + str(chapter) + '/'
    page = requests.get(url, verify=False).text
    soup = bs.BeautifulSoup(page, 'lxml')
    script = soup.find('div', class_='font-size-16 roboto').text
    script = re.sub(r'[^a-zA-Z]', ' ', script)
    script = word_tokenize(script)
    filtered_script = [w.lower() for w in script if w not in stop_words]
    filtered_script = [w for w in filtered_script if len(w) > 2]
    return filtered_script

def get_sentences_from_words(words, len_of_sentences):
	# to convert words into sentences of length len_of_sentence
    sentences = []
    start = 0
    while start+len_of_sentences < len(words):
        sentences.append(' '.join(words[start:start+len_of_sentences]))
        start += len_of_sentences
    if start + len_of_sentences >= len(words):
        sentences.append(' '.join(words[start:]))
    return sentences



all_star_wars_words = []
for movie in star_wars_movies:
    all_star_wars_words += get_movie_script(movie)


potter_words = []
for chapter in range(1, 9):
    potter_words += get_potter_script(chapter)


potter_sentences = get_sentences_from_words(potter_words, 18)
star_wars_sentences = get_sentences_from_words(all_star_wars_words, 18)

document = []
for sentence in star_wars_sentences:
    document.append((sentence, 'star wars'))
for sentence in potter_sentences:
    document.append((sentence, 'harry potter'))


df = pd.DataFrame(columns=['movie', 'sentence'])
for doc in document:
    df = df.append({'movie': doc[1],
                    'sentence': doc[0]}, ignore_index=True)


df.to_csv('star-wars-or-harry-potter.csv')