import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import matplotlib as mpl
import warnings
import sys

# Default output directory for plots
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'results/plots')

# Create the output directory if it doesn't exist
def ensure_output_dir():
    """Make sure the output directory exists"""
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# This allows other modules to change the output directory
def set_output_dir(new_dir):
    """Set a new output directory"""
    global output_dir
    output_dir = new_dir
    return ensure_output_dir()

# Configure plot style for better appearance
sns.set_theme(style="whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Set color palette for better visualization
sns.set_palette("colorblind")

def plot_time_series(data, y_column, title, ylabel, filename):
    """
    Generates and saves a time series line plot.

    Args:
        data (pd.DataFrame): DataFrame containing the time series data. Must have a 'year' column.
        y_column (str or list): The column name(s) for the y-axis data.
        title (str): The title of the plot.
        ylabel (str): The label for the y-axis.
        filename (str): The name of the file to save the plot (without extension).
    """
    if data is None or data.empty:
        print(f"Warning: No data provided for plot '{title}'. Skipping.")
        return None

    if 'year' not in data.columns:
        print(f"Warning: 'year' column not found in data for plot '{title}'. Skipping.")
        return None
    
    # Create a clean copy of the data to avoid warnings
    plot_data = data.copy()

    # Create figure with consistent size
    plt.figure(figsize=(10, 6))
    
    # Plot data based on y_column type
    if isinstance(y_column, list):
        valid_columns = [col for col in y_column if col in plot_data.columns]
        if not valid_columns:
            print(f"Warning: None of the specified columns {y_column} found in data for plot '{title}'. Skipping.")
            plt.close()
            return None
        
        # Use different markers for different lines
        markers = ['o', 's', '^', 'd', 'v', '<', '>', 'p', '*', 'h']
        
        for i, col in enumerate(valid_columns):
            marker = markers[i % len(markers)]
            sns.lineplot(
                x='year', 
                y=col, 
                data=plot_data, 
                marker=marker, 
                markersize=8,
                linewidth=2.5,
                label=col.replace('_', ' ').title()
            )
        plt.legend(frameon=True, framealpha=0.9, facecolor='white', edgecolor='lightgray')
    
    elif isinstance(y_column, str):
        if y_column not in plot_data.columns:
            print(f"Warning: Column '{y_column}' not found in data for plot '{title}'. Skipping.")
            plt.close()
            return None
        
        sns.lineplot(
            x='year', 
            y=y_column, 
            data=plot_data, 
            marker='o',
            markersize=8,
            linewidth=2.5,
            color='#1f77b4'
        )
    else:
        print(f"Warning: Invalid y_column type for plot '{title}'. Skipping.")
        plt.close()
        return None

    # Add a grid for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format the plot
    plt.title(title, fontweight='bold', pad=15)
    plt.xlabel("Year", fontweight='bold')
    plt.ylabel(ylabel, fontweight='bold')
    
    # Make sure we show all years without overcrowding
    years = plot_data['year'].unique()
    if len(years) <= 15:  # Only show all ticks if not too many
        plt.xticks(years, rotation=45 if len(years) > 10 else 0)
    
    # Add a subtle box around the plot
    plt.box(True)
    
    # Make sure everything fits
    plt.tight_layout()
    
    # Ensure output directory exists and normalize filename
    ensure_output_dir()
    
    # Make sure filename doesn't already have a .png extension
    if filename.endswith('.png'):
        clean_filename = filename
    else:
        clean_filename = f"{filename}.png"
    
    # Create the full filepath
    filepath = os.path.join(output_dir, clean_filename)
    
    # Save with high quality
    plt.savefig(filepath, bbox_inches='tight')
    print(f"Plot saved to {filepath}")
    plt.close() # Close the figure to free memory
    
    return filepath

def plot_distribution(data, column, title, xlabel, filename):
    """
    Generates and saves a histogram/distribution plot for a specific year or aggregated.

    Args:
        data (pd.DataFrame or pd.Series): Data containing the variable to plot.
        column (str): The column name for the data.
        title (str): The title of the plot.
        xlabel (str): The label for the x-axis.
        filename (str): The name of the file to save the plot (without extension).
    """
    if data is None or data.empty:
        print(f"Warning: No data provided for plot '{title}'. Skipping.")
        return None

    plt.figure(figsize=(9, 6))
    # Handle DataFrame or Series input
    if isinstance(data, pd.DataFrame) and column in data.columns:
        plot_data = data[column].dropna()
    elif isinstance(data, pd.Series):
        plot_data = data.dropna()
    else:
        print(f"Warning: Column '{column}' not found or empty in data for plot '{title}'. Skipping.")
        plt.close()
        return None
    
    if plot_data.empty:
        print(f"Warning: No valid data for plot '{title}' after removing NaN values. Skipping.")
        plt.close()
        return None

    # Create a more appealing histogram
    sns.histplot(
        plot_data, 
        kde=True, 
        color='#3274A1',
        edgecolor='white',
        alpha=0.7,
        bins=min(30, max(10, int(len(plot_data) / 20))),  # Adaptive bin size
        line_kws={'linewidth': 2, 'color': '#E41A1C'}
    )
    
    # Add summary statistics
    mean_val = plot_data.mean()
    median_val = plot_data.median()
    
    # Add vertical lines for mean and median
    plt.axvline(mean_val, color='#E41A1C', linestyle='dashed', linewidth=1.5, alpha=0.9, label=f'Mean: {mean_val:.2f}')
    plt.axvline(median_val, color='#4DAF4A', linestyle='dashed', linewidth=1.5, alpha=0.9, label=f'Median: {median_val:.2f}')
    
    # Format the plot
    plt.title(title, fontweight='bold', pad=15)
    plt.xlabel(xlabel, fontweight='bold')
    plt.ylabel("Frequency", fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend()
    
    # Make sure everything fits
    plt.tight_layout()
    
    # Save the figure
    filepath = os.path.join(output_dir, f"{filename}.png")
    plt.savefig(filepath, bbox_inches='tight')
    print(f"Plot saved to {filepath}")
    plt.close()
    
    return filepath

def plot_correlation_heatmap(data, title, filename):
    """
    Generates and saves a correlation heatmap.

    Args:
        data (pd.DataFrame): DataFrame containing the variables for correlation analysis.
        title (str): The title of the plot.
        filename (str): The name of the file to save the plot (without extension).
    """
    if data is None or data.empty or data.shape[1] < 2:
        print(f"Warning: Insufficient data provided for correlation heatmap '{title}'. Skipping.")
        return None

    # Clean the data - keep only numeric columns and drop NAs
    numeric_data = data.select_dtypes(include=[np.number])
    if numeric_data.shape[1] < 2:
        print(f"Warning: Insufficient numeric data provided for correlation heatmap '{title}'. Skipping.")
        return None

    # Compute correlation matrix
    correlation_matrix = numeric_data.corr()
    
    # Create nice labels for the heatmap
    labels = [col.replace('_', ' ').title() for col in correlation_matrix.columns]
    
    # Create the figure with appropriate size
    plt.figure(figsize=(max(8, correlation_matrix.shape[0] * 0.8), 
                       max(7, correlation_matrix.shape[0] * 0.7)))
    
    # Create the heatmap with more readable formatting
    heatmap = sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={'shrink': 0.8, 'label': 'Correlation Coefficient'},
        annot_kws={"size": 10}
    )
    
    # Set better labels
    plt.xticks(np.arange(len(labels)) + 0.5, labels, rotation=45, ha='right')
    plt.yticks(np.arange(len(labels)) + 0.5, labels, rotation=0)
    
    # Set title with better formatting
    plt.title(title, fontweight='bold', pad=20, fontsize=14)
    
    # Make sure everything fits
    plt.tight_layout()
    
    # Save the figure
    filepath = os.path.join(output_dir, f"{filename}.png")
    plt.savefig(filepath, bbox_inches='tight')
    print(f"Plot saved to {filepath}")
    plt.close()
    
    return filepath

# Add a new function to create geographical choropleth maps for Bangladesh
def plot_bangladesh_choropleth(data, region_column, value_column, title, cmap, filename):
    """
    Creates a choropleth map of Bangladesh using provided regional data.
    Requires geopandas and a Bangladesh shapefile to be installed.
    
    Args:
        data (pd.DataFrame): DataFrame with regional data (must have region_column and value_column)
        region_column (str): Column name for region identifiers (division or district names)
        value_column (str): Column name for the values to plot
        title (str): Title for the plot
        cmap (str): Colormap name to use (e.g., 'YlGnBu', 'Reds', etc.)
        filename (str): Output filename (without extension)
    """
    try:
        import geopandas as gpd
    except ImportError:
        print("Warning: geopandas is not installed. Bangladesh choropleth mapping is not available.")
        return None
    
    # Check for data validity
    if data is None or data.empty or region_column not in data.columns or value_column not in data.columns:
        print(f"Warning: Invalid data for choropleth map '{title}'. Skipping.")
        return None
    
    # Look for Bangladesh shapefile in standard locations
    shapefile_paths = [
        'data/geodata/bgd_adm1.shp',  # Division level
        'data/external/geodata/bgd_adm1.shp',
        'data/geodata/bgd_adm2.shp',   # District level
        'data/external/geodata/bgd_adm2.shp'
    ]
    
    bd_map = None
    for path in shapefile_paths:
        try:
            if os.path.exists(path):
                bd_map = gpd.read_file(path)
                print(f"Using shapefile: {path}")
                break
        except Exception as e:
            print(f"Error reading shapefile {path}: {e}")
    
    if bd_map is None:
        print("Warning: Bangladesh shapefile not found. Choropleth map cannot be created.")
        return None
    
    # Attempt to merge data with map
    # Normalize column names for better matching
    clean_region_name = lambda x: str(x).lower().strip().replace(' ', '_')
    
    # Clean data regions
    data = data.copy()
    data['region_clean'] = data[region_column].apply(clean_region_name)
    
    # Try to find matching column in geodata
    match_found = False
    for col in bd_map.columns:
        if col.lower() in ['name_1', 'name_2', 'name', 'division', 'district', 'adm1_en', 'adm2_en']:
            bd_map['region_clean'] = bd_map[col].apply(clean_region_name)
            merged_map = bd_map.merge(data, on='region_clean', how='left')
            match_found = True
            break
    
    if not match_found:
        print("Warning: Could not find matching region columns between data and shapefile.")
        return None
    
    # Plot the map
    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    
    # Plot the choropleth
    merged_map.plot(
        column=value_column,
        ax=ax,
        legend=True,
        cmap=cmap,
        missing_kwds={'color': 'lightgray'},
        legend_kwds={
            'label': value_column.replace('_', ' ').title(),
            'orientation': "horizontal",
            'shrink': 0.6,
            'pad': 0.01,
            'fraction': 0.046
        }
    )
    
    # Add labels for regions if not too many
    if len(bd_map) <= 10:  # Only label divisions, not districts
        for idx, row in merged_map.iterrows():
            label = row[region_column] if region_column in row else \
                    row.get('NAME_1', row.get('NAME_2', ''))
            if label:
                ax.annotate(
                    text=label,
                    xy=(row.geometry.centroid.x, row.geometry.centroid.y),
                    ha='center',
                    fontsize=8,
                    color='black',
                    fontweight='bold'
                )
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_axis_off()
    
    # Add title
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Save the plot
    filepath = os.path.join(output_dir, f"{filename}.png")
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    print(f"Plot saved to {filepath}")
    plt.close()
    
    return filepath

def plot_market_dynamics(data, price_column, volatility_column, title, filename):
    """
    Generates and saves a market dynamics plot showing price trends and market stability index.

    Args:
        data (pd.DataFrame): DataFrame containing the market data. Must have 'year' column.
        price_column (str): Column name for price data.
        volatility_column (str): Column name for market volatility/stability.
        title (str): The title of the plot.
        filename (str): The name of the file to save the plot (without extension).
    """
    if data is None or data.empty:
        print(f"Warning: No data provided for market dynamics plot '{title}'. Skipping.")
        return None

    if 'year' not in data.columns or price_column not in data.columns or volatility_column not in data.columns:
        print(f"Warning: Required columns missing in data for market dynamics plot '{title}'. Skipping.")
        return None
    
    # Create a clean copy of the data to avoid warnings
    plot_data = data.copy()

    # Create figure with two y-axes
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Price trend on the first y-axis
    color = '#1f77b4'  # Blue
    ax1.set_xlabel('Year', fontweight='bold')
    ax1.set_ylabel(f'{price_column.replace("_", " ").title()}', color=color, fontweight='bold')
    ax1.plot(plot_data['year'], plot_data[price_column], marker='o', markersize=8, 
             linewidth=3, color=color, label=price_column.replace('_', ' ').title())
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Add a horizontal line at the mean price
    mean_price = plot_data[price_column].mean()
    ax1.axhline(y=mean_price, linestyle='--', color=color, alpha=0.5, 
                label=f'Average Price: {mean_price:.2f}')
    
    # Create a second y-axis for volatility/stability
    ax2 = ax1.twinx()
    color = '#ff7f0e'  # Orange
    ax2.set_ylabel(f'{volatility_column.replace("_", " ").title()}', color=color, fontweight='bold')
    ax2.plot(plot_data['year'], plot_data[volatility_column], marker='s', markersize=8, 
             linewidth=3, color=color, label=volatility_column.replace('_', ' ').title())
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', frameon=True, 
               framealpha=0.9, facecolor='white', edgecolor='lightgray')
    
    # Add annotations for trends
    first_year = plot_data['year'].min()
    last_year = plot_data['year'].max()
    first_price = plot_data[plot_data['year'] == first_year][price_column].values[0]
    last_price = plot_data[plot_data['year'] == last_year][price_column].values[0]
    
    price_change_pct = ((last_price - first_price) / first_price) * 100
    price_direction = "increased" if price_change_pct > 0 else "decreased"
    
    # Add annotation text for price change
    plt.annotate(f"{price_column.replace('_', ' ').title()} {price_direction} by {abs(price_change_pct):.1f}%",
                xy=(last_year, last_price),
                xytext=(10, 20),
                textcoords="offset points",
                bbox=dict(boxstyle="round,pad=0.3", fc="#e0f3f8", ec="#aaaaaa", alpha=0.8),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    
    # Add grid for better readability
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # Title and layout
    plt.title(title, fontweight='bold', pad=15)
    fig.tight_layout()
    
    # Make sure we show all years without overcrowding
    years = plot_data['year'].unique()
    if len(years) <= 15:  # Only show all ticks if not too many
        ax1.set_xticks(years)
        ax1.set_xticklabels(years, rotation=45 if len(years) > 10 else 0)
    
    # Ensure output directory exists and normalize filename
    ensure_output_dir()
    
    # Make sure filename doesn't already have a .png extension
    if filename.endswith('.png'):
        clean_filename = filename
    else:
        clean_filename = f"{filename}.png"
    
    filepath = os.path.join(output_dir, clean_filename)
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()
    print(f"Market dynamics plot saved to {filepath}")
    
    return filepath


def plot_correlation_scatter(data, columns, title, filename, color_by_year=True):
    """
    Creates a scatter plot matrix showing correlations between multiple indicators.
    
    Args:
        data (pd.DataFrame): DataFrame containing the variables for correlation analysis.
        columns (list): List of column names to include in the analysis.
        title (str): The title of the plot.
        filename (str): The name of the file to save the plot (without extension).
        color_by_year (bool): Whether to color points by year for temporal analysis.
    """
    if data is None or data.empty:
        print(f"Warning: No data provided for correlation scatter plot '{title}'. Skipping.")
        return None
    
    # Verify all columns exist
    missing_cols = [col for col in columns if col not in data.columns]
    if missing_cols:
        print(f"Warning: These columns are missing in the data: {missing_cols}. Skipping.")
        return None
    
    # Create a clean copy of the data with just the needed columns
    plot_data = data[columns].copy()
    
    # If we're coloring by year, make sure it's in the data
    year_column = None
    if color_by_year and 'year' in data.columns:
        year_column = 'year'
        plot_data[year_column] = data['year']
    
    # Create a custom colormap for years if needed
    if year_column:
        # Create a colormap that goes from light blue to dark blue
        years = plot_data[year_column].unique()
        if len(years) > 1:
            norm = plt.Normalize(years.min(), years.max())
            sm = plt.cm.ScalarMappable(cmap="viridis", norm=norm)
            sm.set_array([])
    
    # Create the scatter plot matrix
    fig = plt.figure(figsize=(3*len(columns), 3*len(columns)))
    
    # Create a custom scatter plot matrix with more control than pairplot
    n_cols = len(columns)
    grid = plt.GridSpec(n_cols, n_cols, wspace=0.3, hspace=0.3)
    
    for i, col1 in enumerate(columns):
        for j, col2 in enumerate(columns):
            ax = fig.add_subplot(grid[i, j])
            
            # Diagonal: show histograms
            if i == j:
                sns.histplot(plot_data[col1], kde=True, color='#1f77b4', ax=ax)
                ax.set_title(col1.replace('_', ' ').title(), fontsize=10, fontweight='bold')
                continue
            
            # Off-diagonal: scatter plots
            if year_column:
                scatter = ax.scatter(plot_data[col2], plot_data[col1], 
                          c=plot_data[year_column], cmap='viridis', 
                          alpha=0.7, edgecolor='w', s=50)
            else:
                ax.scatter(plot_data[col2], plot_data[col1], 
                          color='#1f77b4', alpha=0.7, edgecolor='w', s=50)
            
            # Add correlation coefficient
            corr = plot_data[col1].corr(plot_data[col2])
            ax.annotate(f'r = {corr:.2f}', xy=(0.05, 0.95), xycoords='axes fraction',
                       fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
            
            # Only show axis labels on the edges
            if i == n_cols-1:
                ax.set_xlabel(col2.replace('_', ' ').title(), fontsize=10)
            else:
                ax.set_xlabel('')
                
            if j == 0:
                ax.set_ylabel(col1.replace('_', ' ').title(), fontsize=10)
            else:
                ax.set_ylabel('')
    
    # Add a colorbar for year coloring if used
    if year_column:
        cbar_ax = fig.add_axes([0.92, 0.3, 0.02, 0.4])  # [left, bottom, width, height]
        cbar = fig.colorbar(sm, cax=cbar_ax)
        cbar.set_label('Year', fontweight='bold')
    
    # Add overall title
    plt.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    
    # Ensure output directory exists and normalize filename
    ensure_output_dir()
    
    # Make sure filename doesn't already have a .png extension
    if filename.endswith('.png'):
        clean_filename = filename
    else:
        clean_filename = f"{filename}.png"
    
    filepath = os.path.join(output_dir, clean_filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)  # Higher DPI for this detailed plot
    plt.close()
    print(f"Correlation scatter plot saved to {filepath}")
    
    return filepath


# Example usage (can be run if this file is executed directly)
if __name__ == '__main__':
    print(f"Visualization functions defined. Plots will be saved in '{output_dir}'")
    
    # Create dummy data for testing
    years = range(2025, 2036)
    dummy_data = pd.DataFrame({
        'year': years,
        'rice_production': [35 + i * 0.5 + np.random.randn() * 0.5 for i in range(len(years))],
        'wheat_production': [1 + i * 0.1 + np.random.randn() * 0.2 for i in range(len(years))],
        'food_prices': [90 + i * 2 + np.random.randn() * 4 for i in range(len(years))],
        'stunting_rate': [0.28 - i * 0.005 + np.random.randn() * 0.01 for i in range(len(years))],
        'wasting_rate': [0.15 - i * 0.003 + np.random.randn() * 0.008 for i in range(len(years))],
        'energy_intake': [1800 + i * 15 + np.random.randn() * 30 for i in range(len(years))]
    })
    
    dummy_dist_data = pd.DataFrame({
        'income_final_year': np.random.lognormal(mean=np.log(2500), sigma=0.4, size=1000)
    })

    # Test plot functions
    plot_time_series(
        data=dummy_data, 
        y_column=['rice_production', 'wheat_production'],
        title='Simulated Cereal Production Over Time', 
        ylabel='Production (Million Tonnes)', 
        filename='cereal_production_ts'
    )
    
    plot_time_series(
        data=dummy_data, 
        y_column='stunting_rate',
        title='Simulated Stunting Rate Over Time', 
        ylabel='Prevalence Rate', 
        filename='stunting_rate_ts'
    )
    
    plot_time_series(
        data=dummy_data, 
        y_column='wasting_rate',
        title='Simulated Wasting Rate Over Time', 
        ylabel='Prevalence Rate', 
        filename='wasting_rate_ts'
    )
    
    plot_time_series(
        data=dummy_data, 
        y_column='energy_intake',
        title='Simulated Energy Intake Over Time', 
        ylabel='Energy (kcal/person/day)', 
        filename='energy_intake_ts'
    )
    
    plot_time_series(
        data=dummy_data, 
        y_column='food_prices',
        title='Simulated Rice Price Over Time', 
        ylabel='Price (Taka/kg)', 
        filename='rice_price_ts'
    )

    plot_distribution(
        data=dummy_dist_data, 
        column='income_final_year', 
        title='Distribution of Household Income (Final Year)', 
        xlabel='Income (USD/capita)', 
        filename='income_distribution_hist'
    )
    
    # Create a heatmap with all the time series variables
    plot_correlation_heatmap(
        data=dummy_data[['rice_production', 'wheat_production', 'food_prices', 'stunting_rate', 'wasting_rate', 'energy_intake']],
        title='Correlation Between Key Indicators',
        filename='indicator_correlation_heatmap'
    )

    # Create dummy division-level data for Bangladesh
    try:
        dummy_division_data = pd.DataFrame({
            'division': ['Dhaka', 'Chittagong', 'Khulna', 'Rajshahi', 'Barisal', 'Sylhet', 'Rangpur', 'Mymensingh'],
            'food_insecurity': [0.22, 0.28, 0.25, 0.30, 0.35, 0.27, 0.32, 0.29]
        })
        
        plot_bangladesh_choropleth(
            data=dummy_division_data,
            region_column='division',
            value_column='food_insecurity',
            title='Food Insecurity by Division',
            cmap='YlOrRd',
            filename='food_insecurity_map'
        )
    except Exception as e:
        print(f"Skipping choropleth map example: {e}")

    print("Test plots generated.")

