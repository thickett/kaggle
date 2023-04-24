import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

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
        pass

    def categorical_pre_process(self):
        pass

    def output_pre_process(self):
        # idea here is we use this to call the other three functions and use their outputs to update
        # a copied version of the dataframe
        # then return this dataframe. That way we only copy the dataframe once, and then make one set
        # of changes, and return the new dataframe.
        pass