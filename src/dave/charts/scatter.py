import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def plot_scatter(x_series, y_series, x_label='X', y_label='Y', title='Scatter Plot', 
                 show_regression=True, show_correlation=True, figsize=(10, 6)):
    """
    Create a scatter plot from two pandas Series or numpy arrays.
    
    Parameters:
    -----------
    x_series : pandas Series or numpy array
        X-axis data
    y_series : pandas Series or numpy array  
        Y-axis data
    x_label : str, optional
        Label for x-axis (default: 'X')
    y_label : str, optional
        Label for y-axis (default: 'Y')
    title : str, optional
        Plot title (default: 'Scatter Plot')
    show_regression : bool, optional
        Whether to show regression line (default: True)
    show_correlation : bool, optional
        Whether to show correlation coefficient (default: True)
    figsize : tuple, optional
        Figure size (default: (10, 6))
    """
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    import numpy as np
    
    # Convert to numpy arrays if needed
    x = np.array(x_series)
    y = np.array(y_series)
    
    # Create the plot
    plt.figure(figsize=figsize)
    plt.scatter(x, y, alpha=0.6, s=50, c='blue', edgecolors='black', linewidth=0.5)
    
    # Add zero axis lines
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.7)
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8, alpha=0.7)
    
    # # Add regression line if requested
    # if show_regression:

    
    # Add correlation coefficient if requested
    if show_correlation:
        correlation = np.corrcoef(x, y)[0, 1]
        plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Customize the plot
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

