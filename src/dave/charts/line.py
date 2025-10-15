import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_line(*series, title='Line Chart', figsize=(12, 6)):
    """
    Create a simple line chart from one or more pandas Series, DataFrames, or numpy arrays.
    Uses the actual index for x-axis and series/column names for the legend.
    
    Parameters:
    -----------
    *series : pandas Series, DataFrame, or numpy arrays
        One or more data series to plot
    title : str, optional
        Plot title (default: 'Line Chart')
    figsize : tuple, optional
        Figure size (default: (12, 6))
    """
    
    plt.figure(figsize=figsize)
    
    # Plot each series
    for i, series in enumerate(series):
        # Handle pandas DataFrame
        if isinstance(series, pd.DataFrame):
            for col in series.columns:
                y = series[col].values
                x = series.index  # Use DataFrame index
                plt.plot(x, y, label=col)
        
        # Handle pandas Series
        elif isinstance(series, pd.Series):
            y = series.values
            x = series.index  # Use Series index
            label = series.name if series.name is not None else f'Series {i+1}'
            plt.plot(x, y, label=label)
        
        # Handle 2D numpy array
        elif isinstance(series, np.ndarray) and series.ndim == 2:
            for j in range(series.shape[1]):
                y = series[:, j]
                x = np.arange(len(y))  # No index available, use range
                plt.plot(x, y, label=f'Column {j+1}')
        
        # Handle 1D numpy array or list
        else:
            y = np.array(series)
            x = np.arange(len(y))  # No index available, use range
            plt.plot(x, y, label=f'Series {i+1}')
    
    # Customize the plot
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()