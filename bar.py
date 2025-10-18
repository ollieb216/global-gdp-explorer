'''
File: bar.py
Author: Oliver Baccay
Description: Visualizes GDP component percentages for top economies as stacked bar charts
'''

import plotly.express as px

def _format_df(df,year,top):
    """ format the dataframe from a wide to long format, clean column names, and calculate the net exports"""
    df_year = df[df["Time"] == year].head(top)
    components = ["Consumption (%)", "Government (%)", "Investments (%)", "Exports (%)", "Imports (%)"]

    # using melt to format to long
    df_long = df_year.melt(id_vars=["Country", "GDP ($)"], value_vars=components, var_name="Component", value_name="Percent").copy()

    # calculate net exports (exports-imports)
    net_exports = df_year["Exports (%)"].values - df_year["Imports (%)"].values
    df_long.loc[df_long["Component"] == "Exports (%)", "Percent"] = net_exports #use exports as new net col
    df_long = df_long[df_long["Component"] != "Imports (%)"] #remove imports

    # clean component names
    df_long["Component"] = df_long["Component"].replace({
        "Consumption (%)": "Consumption",
        "Government (%)": "Government",
        "Investments (%)": "Investment",
        "Exports (%)": "Net Exports"})

    return df_long

def make_bar(df, year, top, **kwargs):
    """ Make stacked bar graph """
    width = kwargs.get('width', 1200)
    height = kwargs.get('height', 800)

    df = _format_df(df,year,top)

    fig = px.bar(df, x="Country", y="Percent", color="Component", title=f"GDP Component Breakdown ({year}) - Top {top} Economies",
                 barmode="stack", height=height, width=width)
    fig.update_layout(yaxis_title="Percent of GDP", xaxis_title="Country", legend_title="Components")

    return fig


def show_bar(df, year, top):
    """ Uses the make_bar function and shows the bar graph"""
    fig = make_bar(df, year, top)
    fig.show()