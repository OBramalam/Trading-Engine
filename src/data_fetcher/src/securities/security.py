from ..common.enums import AssetClass, Sector


class Security:
    def __init__(
            self, 
            ticker, 
            name, 
            listed, 
            asset_class: AssetClass, 
            country,
            datasource, 
            datasource_ticker
    ):
        self.ticker = ticker
        self.name = name
        self.listed = listed
        self.asset_class = asset_class
        self.country = country
        self.datasource = datasource
        self.datasource_ticker = datasource_ticker

    