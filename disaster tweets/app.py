import matplotlib.pyplot as plt
import numpy as np
from shiny import App,ui, render



app_ui = ui.page_fluid(
    ui.input_slider("n","choose a number n:",0,100,40),
    ui.output_text_verbatim("txt"),
)

def server(input,output,session):
    @output
    @render.text
    def txt():
        return f"The currrently selected value of n is: {input.n()}"

app = App(app_ui,server)
