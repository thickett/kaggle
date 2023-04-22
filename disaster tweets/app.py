import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App, reactive
from shiny.types import FileInfo
import pandas as pd

settings = {

    "table_layout":"table"
}



app_ui = ui.page_fluid(
    #navigation bar
    ui.navset_pill_card(
    

    # data import page
    ui.nav("Data page",
           ui.panel_title("Data import and description"),
           ui.layout_sidebar(
                ui.panel_sidebar(
    # ui element to allow users to upload a single file
                        ui.input_file("input_data","Choose a CSV file",
                                      accept=["csv"],multiple=False),
                        ui.input_checkbox("header","Header",True),
        # reactive button to allow users to re-load a different sample from the data.
                        ui.input_action_button("Rerun_sample","New Sample",class_="btn-primary")
                ),
                ui.panel_main(
    #ui output element which we will call in the server to fill with our dataframe.
                        ui.output_ui("contents")
                )
    # next part of the UI is for column statistics and descriptions
           ),ui.panel_title("Data Description"),
           ui.layout_sidebar(
    
                ui.panel_sidebar(
    # create a select object but with [] values. i.e we will dynamically update these depending on the cols.
                    ui.input_select("dtype_select","Select a datatype to explore further.",[])
                ),
                ui.panel_main()
           )
           
           
           
           ),
    ui.nav("EDA")
    )

)

global_data = {}

def server(input, output, session):
    # server code to display the dataframe, and reactively update it if a new sampleis called.
    @output
    @render.ui
    def contents():
        if input.input_data() is None:
            return "Please upload a CSV"
        f: list[FileInfo] = input.input_data()
        df = pd.read_csv(f[0]["datapath"], header=0 if input.header() else None)

        # Store the dataframe in the global dictionary
        global_data['df'] = df

        # Call the dtype_select function explicitly
        dtype_select()

        if input.Rerun_sample is None:
            df_head = df.head(10)
            return ui.HTML(df_head.to_html(classes=settings["table_layout"]))

        input.Rerun_sample()
        with reactive.isolate():
            return ui.HTML(df.sample(10).to_html(classes=settings["table_layout"]))

    # function uses to dynmaically fill the dtype_select select button. 
    # notice how we call this function within the contents function and how we dont set any
    #handles on this. We do define it as an Effect function below though!
    def dtype_select():
        # Access the dataframe from the global dictionary
        df = global_data.get('df')
        if df is not None:
            ui.update_select(
            "dtype_select",  # Update the id parameter to match the input_select id
            choices = [str(dtype) for dtype in set(df.dtypes)]
        )

    # Register the dtype_select function as a reactive effect
    reactive.Effect(dtype_select)

app = App(app_ui, server)

