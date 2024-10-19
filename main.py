import pandas as pd
from taipy.gui import Gui


df = pd.read_csv('global_income_inequality.csv')

print(df.columns)

countries = df['Country'].unique().tolist()

selected_country = countries[0]

area_data = {
    "Year": df["Year"].tolist(),
    "Top 10% Income Share": df["Top 10% Income Share (%)"].tolist(),
    "Bottom 10% Income Share": df["Bottom 10% Income Share (%)"].tolist()
}

scatter_data = {
    "Average Income (USD)":df["Average Income (USD)"].tolist(),
    "Gini Index": df["Gini Index"].tolist()
}

options = [
    # (Bottom 10% Income Share)
    {"fill": "tozeroy"},
    # (Top 10% Income Share)
    {"fill": "tonexty"}
]

def get_filtered_data(country):
    country_data = df[df['Country'] == country]
    return{
        'year': country_data['Year'].tolist(),
        'gini index': country_data['Gini Index'].tolist(),
        # 'series': [country] * len(country_data)
    }

def get_avarage_income(country):
    country_data = df[df['Country'] == country]
    return{
        'year': country_data['Year'].tolist(),
        'average income (USD)': country_data['Average Income (USD)'].tolist(),
        # 'series': [country] * len(country_data)
    }


gini_data = get_filtered_data(selected_country)
anual_income_data = get_avarage_income(selected_country)

page1_md="""
<|{df}|table|>
"""
page2_md = """
# Income Inequality Analysis

Choose country: <|{selected_country}|selector|lov={countries}|on_change=update_data|dropdown|>
<|layout|columns=1 1|

<|first column
<|{gini_data}|chart|type=line|x=year|y=gini index|title=Income Inequality Over Time|>
|>

<|second column
<|{anual_income_data}|chart|type=waterfall|x=year|y=average income (USD)|title=Average Income Over Time|>
|>

<|first column second row
<|{area_data}|chart|mode=none|x=Year|y[1]=Bottom 10% Income Share|y[2]=Top 10% Income Share|options={options}|title=Stacked Area Chart of Income Share Over Time|>
|>

<|second column second row
<|{scatter_data}|chart|mode=markers|x=Average Income (USD)|y=Gini Index|title=Scatter Plot of Gini Index vs. Average Income|>
|>

|>
"""

def update_data(state):
    state.gini_data = get_filtered_data(state.selected_country)
    state.anual_income_data = get_avarage_income(state.selected_country)


root_md = "<|navbar|>"
pages = {
    "/": root_md,
    "Data": page1_md,
    "Visualization": page2_md 
}

gui = Gui(pages=pages).run()