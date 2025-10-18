'''
File: gdpexplorer.py
Author: Oliver Baccay
Description: Interactive dashboard for exploring global GDP components and trends
'''

import panel as pn
from gdpAPI import GDPAPI
import donut as dn
import bar
import pandas as pd

# Loads javascript dependencies and configures Panel (required)
pn.extension()

api = GDPAPI()
api.load_gdpdata('data/gdp.csv')


# WIDGET DECLARATIONS

# Search Widgets
year = pn.widgets.DiscreteSlider(name='Year', options=list(range(2014, 2025)), value=2022)
country = pn.widgets.Select(name='Select Country', options=api.get_countries(), value='United States')
top = pn.widgets.IntSlider(name='Top Economies', start=1, end=150, value=30)

# Plotting Widgets
b_width = pn.widgets.IntSlider(name="Width", start=250, end=1400, step=50, value=1400)
b_height = pn.widgets.IntSlider(name="Height", start=200, end=700, step=50, value=400)

d_width = pn.widgets.IntSlider(name="Width", start=550, end=800, step=50, value=700)
d_height = pn.widgets.IntSlider(name="Height", start=300, end=700, step=50, value=400)


# CALLBACK FUNCTIONS
def get_catalog(year, top):
    df = api.extract_top_gdpdata(year, top)
    table = pn.widgets.Tabulator(df, selectable=False)
    return table

def get_donut(country, year, width, height):
    df = api.extract_gdpdata(year)

    df_country = df[df["Country"] == country]

    # No data for country/year's gdp
    if pd.isna(df_country["GDP ($)"]).all():
        return pn.pane.Markdown(f"### GDP value missing for {country} in {year}")

    gdp_cols = ["Consumption (%)", "Government (%)", "Investments (%)", "Exports (%)", "Imports (%)"]
    if df_country[gdp_cols].isna().all(axis=1).iloc[0]:
        return pn.pane.Markdown(f"### GDP components missing for {country} in {year} | GDP: {dn.scale_gdp(df, country, year)}")

    fig = dn.make_donut(df, country, year, height=height, width=width)
    return fig


def get_bar(year, top, width, height):
    df = api.extract_top_gdpdata(year, top)
    fig = bar.make_bar(df, year, top, height=height, width=width)
    return fig


# CALLBACK BINDINGS (Connecting widgets to callback functions)
catalog = pn.bind(get_catalog, year, top)
donut = pn.bind(get_donut, country, year, d_width, d_height)
world_donut = pn.bind(get_donut, 'World', year, d_width, d_height)
bar_plot = pn.bind(get_bar, year, top, b_width, b_height)

# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

year_card = pn.Card(
    pn.Column(
        year
    ),
    title="Select Year", width=card_width, collapsed=False
)
search_card = pn.Card(
    pn.Column(
        # Widget 1
            top,
        # Widget 2
            b_width,
        # Widget 3
            b_height
    ),
    title="Bar Plot", width=card_width, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        # Widget 1
        country,
        d_width,
        d_height
    ),

    title="Donut Plots", width=card_width, collapsed=False
)


# LAYOUT
layout = pn.template.FastListTemplate(
    title="Gross Domestic Product Explorer",
    sidebar=[
        year_card,
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Data", catalog),
            ("Graphs",
                pn.Column(
                        bar_plot,
                pn.Row(world_donut,
                       donut,
                    sizing_mode="stretch_width")
                    )
             ),
            active=1
        )

    ],
    header_background='#a93226'

).servable()

layout.show()


