import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App, reactive


app_ui = ui.page_fluid(


)



def server(input,output,session):
    pass

app = App(app_ui,server)