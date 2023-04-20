from shiny import App,ui



app_ui = ui.page_fluid(
    ui.input_slider("n","choose a number n:",0,100,40)
)

def server(input,output,session):
    pass

app = App(app_ui,server)
