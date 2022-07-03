import nltk
from nltk.corpus import stopwords
import codecs


def cleaning():
    with codecs.open("C:/Users/Supun/PycharmProjects/Tagger2/Text_Files/inputText.txt", encoding='utf-8') as f:
        text = f.read()
    sentences = nltk.sent_tokenize(text)  # Text will be tokenized in to sentences
    stop_words = set(stopwords.words("sinhala"))
    phrases = []

    for line in sentences:
        words = nltk.word_tokenize(line)  # each sentence is tokenizing in to words
        cleaned_text = " ".join(list(filter(lambda x: x not in stop_words, words)))  # Removing stop words
        # words ="".join(list(filter(lambda x: x not in string.punctuation, cleaned_text))) #Removing punctuation marks
        # phrases.append(words)
        phrases.append(cleaned_text)
        # words = ''
    return phrases













