import re
import unicodedata
import pandas as pd
import unidecode
from nltk import word_tokenize

class TextCleaner():
    def __init__(self):
        self.stop_words_list = pd.read_csv('./resources/it-stopwords.csv')['STOPWORDS'].values.tolist()
        self.it_names = pd.read_csv("./resources/it-names.csv")['NOMI'].values.tolist()

    def strip_accents(self, text):

        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

        return str(text)

    def clean(self, text):
        def contains_symbol(word):
            return re.search("[^a-zA-Z]", word)

        def is_name(word):
            return word.capitalize() in self.it_names

        def is_stopword(word):
            return word in self.stop_words_list

        def is_link(word):
            return re.search("https?", word)

        clean_tokenized_sentence = list()

        # To lower case
        clean = str(text).lower()

        # Italian language has accents. Substitute each of them with the corresponding non-accented. (es. à -> a)
        clean = unidecode.unidecode(clean)

        # Trim spaces from start and end
        clean = clean.strip()

        # Remove tagged profiles
        clean = re.sub("@[^ ]+( |\Z)", '', clean)

        # Remove hashtags
        clean = re.sub("#[^ ]+( |\Z)", '', clean)

        # Remove parola altro alla fine
        clean = re.sub(" \.\.\.altro\.\.\.", '', clean)

        # Remove elision forms (i.e. "d'altronde", "l'altro")
        clean = re.sub("[^ ]'(.)", r'\1', clean)

        # Remove internal additional spaces (=substitute two or more consecutive spaces with one single space)
        clean = re.sub(" {2,}", ' ', clean)

        tokenized_sentence = word_tokenize(clean)

        i = 0
        while i < len(tokenized_sentence): #Each element of the list "tokenized_sentence" is a word
            word = tokenized_sentence[i]
            i += 1
            if not(len(word) < 3 or contains_symbol(word) or is_link(word) or is_name(word) or is_stopword(word)):
                clean_tokenized_sentence.append(word)

        return " ".join(clean_tokenized_sentence)


if __name__=="__main__":
    cleaner = TextCleaner()
    clean = cleaner.clean("stasera #sera http://www.sera.fake :) Biden è diventato il nuovo presidente")

    print(clean)
