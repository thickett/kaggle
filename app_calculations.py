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
    
