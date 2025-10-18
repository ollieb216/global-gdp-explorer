'''
File: donut.py
Author: Oliver Baccay
Description: Visualizes GDP component percentages for top economies as donut charts
'''

import plotly.graph_objects as go
import pandas as pd


def scale_gdp(df, country, year):
    """Return the gdp in trillions, billions, or millions, depending on how large its economy is"""
    df_year = df[(df["Country"] == country) & (df["Time"] == year)]
    gdp = df_year["GDP ($)"].values[0]

    if gdp >= 1e12:
        return f"${gdp / 1e12:.2f} Trillion"
    elif gdp >= 1e9:
        return f"${gdp / 1e9:.2f} Billion"
    elif gdp >= 1e6:
        return f"${gdp / 1e6:.2f} Million"


def make_donut(df, country, year, **kwargs):
    """ Make the donut chart"""
    df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
    year = int(year)
    df_year = df[(df["Country"] == country) & (df["Time"] == year)].copy()

    labels = ["Consumption (%)", "Government (%)", "Investments (%)", "Exports (%)", "Imports (%)"]
    color_map = {"Consumption (%)": "lightcyan", "Government (%)": "cyan", "Investments (%)": "royalblue", "Exports (%)": "darkblue", "Imports (%)": "lightblue"}

    values = [df_year.get(comp, pd.Series([0])).values[0] or 0 for comp in labels]
    colors = [color_map[label] for label in labels]

    width = kwargs.get('width', 1200)
    height = kwargs.get('height', 800)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker=dict(colors=colors),textinfo="text")]) # to disable the auto percent
    fig.update_traces(hovertemplate="%{label}: %{value:.1f}%<extra></extra>", text=[f"{v:.1f}%" for v in values], textposition="inside") # real percentage when hovering
                                                        #removes trace text

    fig.update_layout(title=f"{country} GDP Components ({year}) | GDP: {scale_gdp(df, country, year)}", height=height, width=width)
    return fig


def show_donut(df, country, year, **kwargs):
    """ Show the donut plot """
    fig=make_donut(df, country, year, **kwargs)
    fig.show()