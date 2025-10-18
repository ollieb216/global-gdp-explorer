'''
gdpAPI.py
Author: Oliver Baccay
Description: Load, extract, and filter GDP data for global GDP info
'''

import pandas as pd

class GDPAPI:
    def __init__(self):
        """ Constructor """
        self.gdpdata = None

    def load_gdpdata(self,filename):
        """Load and store country gdp data"""
        self.gdpdata = pd.read_csv(filename, skipfooter=5, engine='python', na_values=['..'] )

    def get_countries(self):
        """ Get the names of the countries in the dataset"""
        countries = self.gdpdata['Country Name'].dropna().unique()

        return sorted(countries)


    def extract_gdpdata(self, year):
        """ Get the clean table of country gdp data """
        df_year = self.gdpdata[self.gdpdata['Time'] == year].copy()
        series_map = {
            'Country Name': 'Country',
            'GDP (current US$) [NY.GDP.MKTP.CD]': 'GDP ($)',
            'Households and NPISHs final consumption expenditure (% of GDP) [NE.CON.PRVT.ZS]': 'Consumption (%)',
            'General government final consumption expenditure (% of GDP) [NE.CON.GOVT.ZS]': 'Government (%)',
            'Gross capital formation (% of GDP) [NE.GDI.TOTL.ZS]': 'Investments (%)',
            'Exports of goods and services (% of GDP) [NE.EXP.GNFS.ZS]': 'Exports (%)',
            'Imports of goods and services (% of GDP) [NE.IMP.GNFS.ZS]': 'Imports (%)'
        }
        # rename columns
        df_year.rename(columns=series_map, inplace=True)

        df_year.drop(columns=['Country Code', 'Time Code'], inplace=True)  # removing unnecessary columns
        return df_year


    def extract_top_gdpdata(self, year, top):
        """ Get the clean sorted table of country gdp data """
        df_year = self.extract_gdpdata(year)
        topgdp = df_year.sort_values('GDP ($)', ascending=False).head(top)

        return topgdp



def main():
    pass

if __name__ == '__main__':
    main()


