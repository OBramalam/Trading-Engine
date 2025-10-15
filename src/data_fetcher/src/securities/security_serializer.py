import pandas as pd
from typing import List
from .security import Security

class SecuritySerializer:
    def __init__(self, file_path):
        self.file_path = file_path

    def get(self, tickers: List[str]) -> List[Security]:
        df = pd.read_csv(self.file_path)
        securities = []
        
        for ticker in tickers:
            # Filter for the specific ticker
            ticker_data = df[df['ticker'] == ticker]
            
            if len(ticker_data) == 0:
                print(f"Warning: Ticker {ticker} not found in data")
                continue
                
            row = ticker_data.iloc[0]  # Get the first (and should be only) row
            
            security = Security(
                ticker=ticker,
                name=row['name'],
                listed=row['listed'],
                asset_class=row['asset_class'],
                country=row['country'],
                datasource=row['datasource'],
                datasource_ticker=row['datasource_ticker']
            )
            securities.append(security)
        
        return securities

    def get_all(self) -> List[Security]:
        df = pd.read_csv(self.file_path)
        return [Security(
            ticker=row['ticker'],
            name=row['name'],
            listed=row['listed'],
            asset_class=row['asset_class'],
            country=row['country'],
            datasource=row['datasource'],
            datasource_ticker=row['datasource_ticker'],
        ) for index, row in df.iterrows()]

    def save(self, security: Security):

        df = pd.read_csv(self.file_path)
        existing_index = df[df['ticker'] == security.ticker].index
        
        new_row = {
            'ticker': security.ticker,
            'name': security.name,
            'listed': security.listed,
            'asset_class': security.asset_class.value if hasattr(security.asset_class, 'value') else security.asset_class,
            'country': security.country,
            'datasource': security.datasource,
            'datasource_ticker': security.datasource_ticker
        }
        
        if len(existing_index) > 0:
            df.loc[existing_index[0]] = new_row
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_csv(self.file_path, index=False)

        print(f"Security {security.ticker} saved to {self.file_path}")
        return security