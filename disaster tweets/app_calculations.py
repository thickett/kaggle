import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk
import string

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

# set theme for all graphs to be that of seaborn.
sns.set_theme()

def numeric_histogram(col,title,n):
    

    fig, ax = plt.subplots()

    ax.hist(col,bins=n)
    ax.set_title(f"A histogram of the {title} variable.")
    return fig


def categorical_count_plot(col,title,n):
  
    return col[0:n].plot(kind="bar",title=f"Frequency plot of the {title} variable.")
    


#Pre-process

class pre_process():

    def __init__(self,df,numeric_cols,text_cols,categorical_cols):
        self.df = df.copy()
        self.numeric_cols = numeric_cols
        self.text_cols = text_cols
        self.categorical_cols = categorical_cols
    

    def numerical_pre_process(self):

        for col in self.numeric_cols:
            col*2
            return col
    
    def text_pre_process(self):

        '''takes a series of text bodies and tokenizes them, first into sentences, and then to words. 
    It also takes some additional steps to remove stop words and punctuation.
    Parameters
    ----------
    
    text: An array-like of the shape (n_text_documents,)
        An array that contains all the text to be tokenized.
    return
    ----------
    
    filtered_list: list
        A list of lists that contains the tokenized words of each sentence in a body of text.
        '''
        # list to store outputted column(s)
        temp_list = []
        # list to store tokens for a specific column, these will then be appended to temp_list
        # note: temp_list and filtered_list will be the same if on 1 column exists in self.text_cols.
        filtered_list = []

        english_stop_words = stopwords.words("english")
        english_stop_words.extend(["said","would","could","also","get","go","like","try","part","also",
                                "it's","that's","might","people","year","one","says"])
        for col in self.text_cols:
            text = self.df[col]
            for i in text.index:

                sent_tokens = sent_tokenize(text[i].lower())
                removed_punctuation = [i.translate(str.maketrans('','',string.punctuation)) for i in sent_tokens]

                word_tokens = [word_tokenize(i) for i in removed_punctuation]
                filtered = [[word for word in sent if word not in english_stop_words and len(word) >3] for sent in word_tokens ]
                filtered_list.append(filtered)
            temp_list.append(filtered_list)
        return  temp_list

    def categorical_pre_process(self):
        pass

    def output_pre_process(self):
        # idea here is we use this to call the other three functions and use their outputs to update
        # a copied version of the dataframe
        # then return this dataframe. That way we only copy the dataframe once, and then make one set
        # of changes, and return the new dataframe.
        text_columns = self.text_pre_process()