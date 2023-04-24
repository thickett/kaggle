import matplotlib.pyplot as plt
import numpy as np
from shiny import ui, render, App, reactive
from shiny.types import FileInfo
import pandas as pd
from pandas.api.types import is_numeric_dtype
from app_calculations import numeric_histogram, categorical_count_plot

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
                        ui.output_ui("contents"),
                        ui.output_text_verbatim("numeric_var_text"),
                        ui.output_ui("description")
                )
    
    
    
           ),
           # next part of the UI is for column statistics and descriptions
       
           ui.panel_title("Data Description"),
           ui.layout_sidebar(
    
                ui.panel_sidebar(
    # create a select object but with [] values. i.e we will dynamically update these depending on the cols.
                    ui.input_select("column_select","select a column to describe.",[]),
                    ui.input_slider("graph_slide","Change the amount of data to be shown",0,100,1)
                ),
                    
                ui.panel_main(ui.output_plot("histo")
                    
                )
           )
           
           
           
           ),
    ui.nav("Pre Processing",
            ui.panel_title("Pre Processing"),
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_selectize("pre_field_select_numeric","Numeric Fields",[],multiple=True),
                    ui.input_selectize("pre_field_select_categorical","Categorical Fields",[],multiple=True),
                    ui.input_selectize("pre_field_select_text","Text Fields",[],multiple=True),



                    
                ),
                ui.panel_main()
            )
            
            
            
            )
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
        
        column_select()

        if input.Rerun_sample.get() ==0:
            df_head = df.head(10)
            return ui.HTML(df_head.to_html(classes=settings["table_layout"]))

        input.Rerun_sample()
        with reactive.isolate():
            return ui.HTML(df.sample(10).to_html(classes=settings["table_layout"]))
        
    @output
    @render.ui   
    def description():
        df = global_data.get("df")
        
        if input.input_data() is None:
            return 
        desc = df.describe()
        return ui.HTML(desc.to_html(classes=settings["table_layout"]))
    
    @output
    @render.text
    def numeric_var_text():
        if input.input_data() is None:
            return 
        return ui.HTML('General description of numeric fields.')
    
    @output
    @render.plot
    def histo():
        df = global_data.get("df")
        if df is not None:
            
            col_name = input.column_select.get()
            col_data = df[col_name]

            unique_counts = col_data.value_counts()
            slide_input = input.graph_slide.get()
            
            if is_numeric_dtype(col_data):
                n = slide_input*2
                return numeric_histogram(col_data,col_name,n+1)
            else: 
                n = round(len(unique_counts) * slide_input/100)
                return categorical_count_plot(unique_counts,col_name,n+1)
    

    # function uses to dynmaically fill the column_select select button. 
    # notice how we call this function within the contents function and how we dont set any
    #handles on this. We do define it as an Effect function below though!
    def column_select():
        # Access the dataframe from the global dictionary
        df = global_data.get('df')
        if df is not None:
            choices = [str(col) for col in set(df.columns)]
            
            #update select boxes on Data page with col names
            update_select_list = ["column_select" # define select boxes to update
                                  ]
            for selection in update_select_list:
                ui.update_select(
                selection, 
                choices = choices),

            # update selectize boxes in pre page with col names
            update_selectize_list = ["pre_field_select_numeric", # define selectize boxes to update
                                     "pre_field_select_categorical",
                                     "pre_field_select_text"]
            for selectize in update_selectize_list:
                ui.update_selectize(
                selectize,
                choices=choices),
            
    # Register the column_select function as a reactive effect
    reactive.Effect(column_select)


    ## EDA Page server


  
app = App(app_ui, server)

