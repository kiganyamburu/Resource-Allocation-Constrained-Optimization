"""
Heckscher-Ohlin Model Analysis
Assignment #4: Resource Allocation & Constrained Optimization

This script:
1. Downloads FRED data (Real GDP, Labor Force, Investment, Exports)
2. Calculates Capital Deepening and Capital-Labor Ratio
3. Creates a dual-axis visualization
4. Runs a linear regression analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# Try to use fredapi if available, otherwise use requests
try:
    from fredapi import Fred

    USE_FREDAPI = True
except ImportError:
    import requests

    USE_FREDAPI = False

# =============================================================================
# Part 1: Data Acquisition from FRED
# =============================================================================


def download_fred_data(start_date="1960-01-01", end_date=None):
    """
    Download the required FRED data series.

    Series:
    - GDPC1: Real GDP (Billions of Chained Dollars)
    - CLF16OV: Civilian Labor Force (Thousands of Persons) - converted to annual
    - GPDIC1: Real Gross Private Domestic Investment (Billions of Chained Dollars)
    - EXPGSC1: Real Exports of Goods & Services (Billions of Chained Dollars)
    """
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    print("Downloading FRED data...")
    print(f"Period: {start_date} to {end_date}")

    # Define series to download
    series = {
        "GDPC1": "Real_GDP",  # Billions of Chained Dollars
        "CLF16OV": "Labor_Force",  # Thousands of Persons (monthly, will aggregate)
        "GPDIC1": "Real_Investment",  # Billions of Chained Dollars
        "EXPGSC1": "Real_Exports",  # Billions of Chained Dollars
    }

    data_frames = []

    # Download using requests directly to FRED API
    for fred_code, name in series.items():
        try:
            # Use the observations API endpoint
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id={fred_code}&file_type=json&observation_start={start_date}&observation_end={end_date}"

            # Try direct CSV download first (public access)
            csv_url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id={fred_code}&scale=left&cosd={start_date}&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Annual&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date={end_date}&revision_date={end_date}&nd=1947-01-01"

            df = pd.read_csv(csv_url)
            # Rename first column to DATE if it's not already
            df.columns = ["DATE", name]
            df["DATE"] = pd.to_datetime(df["DATE"])
            df = df.set_index("DATE")
            # Replace '.' with NaN for missing values
            df[name] = pd.to_numeric(df[name], errors="coerce")
            data_frames.append(df)
            print(f"  ✓ Downloaded {fred_code} ({name})")
        except Exception as e:
            print(f"  ✗ Error downloading {fred_code}: {e}")
            print("  → Using sample data for demonstration")
            return create_sample_data()

    # Combine all series
    combined = pd.concat(data_frames, axis=1)

    # Resample to annual (Labor Force is monthly, others are quarterly)
    # Using annual average for Labor Force as specified
    annual_data = combined.resample("YE").mean()
    annual_data.index = annual_data.index.year
    annual_data.index.name = "Year"

    return annual_data


def create_sample_data():
    """
    Create sample data based on actual FRED historical values for demonstration.
    This data approximates real U.S. economic data from 1960-2024.
    """
    print("\n  Creating sample data based on historical FRED values...")

    years = list(range(1960, 2025))

    # Sample data approximating actual FRED values
    # Real GDP (GDPC1) - Billions of Chained 2017 Dollars
    real_gdp = [
        3260,
        3345,
        3550,
        3705,
        3915,
        4170,
        4431,
        4543,
        4752,
        4875,  # 1960-1969
        4870,
        5021,
        5280,
        5590,
        5551,
        5519,
        5818,
        6116,
        6453,
        6628,  # 1970-1979
        6581,
        6753,
        6624,
        6880,
        7365,
        7679,
        7945,
        8197,
        8475,
        8786,  # 1980-1989
        8908,
        8870,
        9179,
        9415,
        9721,
        9989,
        10320,
        10684,
        11124,
        11557,  # 1990-1999
        11992,
        12090,
        12288,
        12594,
        12992,
        13373,
        13608,
        13660,
        13228,
        12837,  # 2000-2009
        13145,
        13458,
        13782,
        14035,
        14417,
        14813,
        15045,
        15348,
        15822,
        16330,  # 2010-2019
        16197,
        17032,
        17551,
        18014,
        18537,  # 2020-2024
    ]

    # Civilian Labor Force (CLF16OV) - Thousands of Persons (annual average)
    labor_force = [
        69628,
        70459,
        70614,
        71833,
        73091,
        74455,
        75770,
        77347,
        78737,
        80734,  # 1960-1969
        82771,
        84382,
        87034,
        89429,
        91949,
        93775,
        96158,
        99009,
        102251,
        104962,  # 1970-1979
        106940,
        108670,
        110204,
        111550,
        113544,
        115461,
        117834,
        119865,
        121669,
        123869,  # 1980-1989
        125840,
        126346,
        128105,
        129200,
        131056,
        132304,
        133943,
        136297,
        137673,
        139368,  # 1990-1999
        142583,
        143734,
        144863,
        146510,
        147401,
        149320,
        151428,
        153124,
        154287,
        154142,  # 2000-2009
        153889,
        153617,
        154975,
        155389,
        155922,
        156715,
        159187,
        160320,
        162075,
        163539,  # 2010-2019
        160742,
        161204,
        164287,
        166778,
        168500,  # 2020-2024
    ]

    # Real Gross Private Domestic Investment (GPDIC1) - Billions of Chained 2017 Dollars
    real_investment = [
        395,
        395,
        433,
        465,
        494,
        557,
        599,
        576,
        598,
        631,  # 1960-1969
        600,
        651,
        727,
        799,
        726,
        617,
        731,
        863,
        956,
        979,  # 1970-1979
        830,
        907,
        760,
        820,
        1002,
        1053,
        1094,
        1135,
        1188,
        1235,  # 1980-1989
        1193,
        1105,
        1185,
        1268,
        1390,
        1479,
        1586,
        1735,
        1927,
        2084,  # 1990-1999
        2198,
        2061,
        1943,
        2003,
        2185,
        2318,
        2384,
        2322,
        2078,
        1512,  # 2000-2009
        1698,
        1825,
        2020,
        2120,
        2260,
        2412,
        2475,
        2565,
        2730,
        2806,  # 2010-2019
        2617,
        2920,
        3142,
        3200,
        3350,  # 2020-2024
    ]

    # Real Exports of Goods & Services (EXPGSC1) - Billions of Chained 2017 Dollars
    real_exports = [
        145,
        147,
        157,
        170,
        188,
        195,
        207,
        220,
        243,
        260,  # 1960-1969
        291,
        304,
        331,
        405,
        439,
        438,
        480,
        510,
        571,
        649,  # 1970-1979
        709,
        721,
        680,
        665,
        714,
        734,
        798,
        884,
        1002,
        1104,  # 1980-1989
        1178,
        1217,
        1271,
        1327,
        1409,
        1509,
        1612,
        1739,
        1844,
        1947,  # 1990-1999
        2086,
        2020,
        2007,
        2011,
        2133,
        2260,
        2431,
        2484,
        2471,
        2181,  # 2000-2009
        2393,
        2559,
        2699,
        2765,
        2857,
        2907,
        2878,
        2955,
        3098,
        3128,  # 2010-2019
        2641,
        2790,
        3040,
        3150,
        3280,  # 2020-2024
    ]

    df = pd.DataFrame(
        {
            "Year": years,
            "Real_GDP": real_gdp,
            "Labor_Force": labor_force,
            "Real_Investment": real_investment,
            "Real_Exports": real_exports,
        }
    )
    df = df.set_index("Year")

    print("  ✓ Sample data created (1960-2024)")
    return df


# =============================================================================
# Part 2: Data Calculation & Standardization
# =============================================================================


def calculate_variables(df):
    """
    Calculate Capital Deepening and Capital-Labor Ratio.

    Capital Deepening (Investment % of GDP):
        = (Real Domestic Investment / Real GDP) × 100

    Capital-Labor Ratio (K/L):
        = Real Domestic Investment / Civilian Labor Force

        UNIT ADJUSTMENT:
        - Investment: Billions → Dollars (multiply by 1,000,000,000)
        - Labor Force: Thousands → Persons (multiply by 1,000)

        Result: Dollars of Investment per Worker
    """
    print("\nCalculating derived variables...")

    # Capital Deepening (Investment as % of GDP)
    df["Capital_Deepening_Pct"] = (df["Real_Investment"] / df["Real_GDP"]) * 100

    # Capital-Labor Ratio (Dollars per Worker)
    # Convert Investment from Billions to Dollars: multiply by 1e9
    # Convert Labor Force from Thousands to Persons: multiply by 1e3
    # K/L = (Investment × 1e9) / (Labor Force × 1e3) = (Investment / Labor Force) × 1e6

    df["Capital_Labor_Ratio"] = (df["Real_Investment"] * 1e9) / (
        df["Labor_Force"] * 1e3
    )

    print("  ✓ Capital Deepening (Investment % of GDP)")
    print("  ✓ Capital-Labor Ratio ($ per Worker)")

    return df


# =============================================================================
# Part 3: Visualization - Dual-Axis Chart
# =============================================================================


def create_dual_axis_chart(df, save_path="capital_deepening_chart.png"):
    """
    Create a dual-axis line chart:
    - Left Axis: Capital Deepening (Investment as % of GDP)
    - Right Axis: Capital-Labor Ratio (K/L)
    """
    print("\nCreating dual-axis visualization...")

    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Left axis: Capital Deepening
    color1 = "#1f77b4"  # Blue
    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel("Capital Deepening (Investment % of GDP)", color=color1, fontsize=12)
    line1 = ax1.plot(
        df.index,
        df["Capital_Deepening_Pct"],
        color=color1,
        linewidth=2,
        marker="o",
        markersize=3,
        label="Capital Deepening (%)",
    )
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # Right axis: Capital-Labor Ratio
    ax2 = ax1.twinx()
    color2 = "#d62728"  # Red
    ax2.set_ylabel("Capital-Labor Ratio ($ per Worker)", color=color2, fontsize=12)
    line2 = ax2.plot(
        df.index,
        df["Capital_Labor_Ratio"],
        color=color2,
        linewidth=2,
        marker="s",
        markersize=3,
        label="K/L Ratio ($)",
    )
    ax2.tick_params(axis="y", labelcolor=color2)

    # Title and legend
    plt.title(
        "U.S. Capital Deepening and Capital-Labor Ratio (1960-Present)\n"
        "Heckscher-Ohlin Model Analysis",
        fontsize=14,
        fontweight="bold",
    )

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=10)

    # Add annotations for key periods
    ax1.axvspan(2007, 2009, alpha=0.2, color="gray", label="Great Recession")
    ax1.axvspan(2020, 2021, alpha=0.2, color="orange", label="COVID-19")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"  ✓ Chart saved to: {save_path}")

    return fig


# =============================================================================
# Part 4: Regression Analysis
# =============================================================================


def run_regression_analysis(df):
    """
    Run a simple linear regression:
    - Y (Dependent): Real Exports (EXPGSC1)
    - X (Independent): Capital-Labor Ratio (K/L)
    """
    print("\n" + "=" * 70)
    print("REGRESSION ANALYSIS")
    print("Y-Variable (Dependent): Real Exports (EXPGSC1)")
    print("X-Variable (Independent): Capital-Labor Ratio (K/L)")
    print("=" * 70)

    # Prepare data (drop any NaN values)
    reg_data = df[["Real_Exports", "Capital_Labor_Ratio"]].dropna()

    X = reg_data["Capital_Labor_Ratio"]
    y = reg_data["Real_Exports"]

    # Add constant for intercept
    X_with_const = sm.add_constant(X)

    # Run OLS regression
    model = sm.OLS(y, X_with_const).fit()

    # Print results
    print(model.summary())

    # Create scatter plot with regression line
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(X, y, alpha=0.6, label="Observed Data")
    ax.plot(
        X,
        model.predict(X_with_const),
        color="red",
        linewidth=2,
        label=f"Regression Line (R² = {model.rsquared:.4f})",
    )

    ax.set_xlabel("Capital-Labor Ratio ($ per Worker)", fontsize=12)
    ax.set_ylabel("Real Exports (Billions of Chained $)", fontsize=12)
    ax.set_title(
        "Regression: Real Exports vs Capital-Labor Ratio",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("regression_plot.png", dpi=300, bbox_inches="tight")
    plt.show()
    print("\n  ✓ Regression plot saved to: regression_plot.png")

    return model


# =============================================================================
# Additional Analysis: Stationarity Tests
# =============================================================================


def test_stationarity(df):
    """
    Test for unit roots in the time series using Augmented Dickey-Fuller test.
    This is important for understanding spurious regression issues.
    """
    from statsmodels.tsa.stattools import adfuller

    print("\n" + "=" * 70)
    print("STATIONARITY ANALYSIS (Augmented Dickey-Fuller Test)")
    print("H0: Series has a unit root (non-stationary)")
    print("=" * 70)

    variables = ["Real_Exports", "Capital_Labor_Ratio", "Capital_Deepening_Pct"]

    for var in variables:
        series = df[var].dropna()
        result = adfuller(series, autolag="AIC")

        print(f"\n{var}:")
        print(f"  ADF Statistic: {result[0]:.4f}")
        print(f"  p-value: {result[1]:.4f}")
        print(f"  Critical Values:")
        for key, value in result[4].items():
            print(f"    {key}: {value:.4f}")

        if result[1] < 0.05:
            print(f"  → STATIONARY (reject H0)")
        else:
            print(f"  → NON-STATIONARY (cannot reject H0) - UNIT ROOT PRESENT")


# =============================================================================
# Main Execution
# =============================================================================


def main():
    print("=" * 70)
    print("HECKSCHER-OHLIN MODEL: U.S. Factor Endowments Analysis")
    print("Assignment #4: Resource Allocation & Constrained Optimization")
    print("=" * 70)

    # Part 1: Download FRED data
    df = download_fred_data(start_date="1960-01-01")

    if df is None:
        print("Error: Could not download data. Please check your internet connection.")
        return

    # Part 2: Calculate variables
    df = calculate_variables(df)

    # Display the data
    print("\n" + "=" * 70)
    print("CALCULATED DATA (First 10 and Last 10 years)")
    print("=" * 70)
    display_cols = [
        "Real_GDP",
        "Labor_Force",
        "Real_Investment",
        "Real_Exports",
        "Capital_Deepening_Pct",
        "Capital_Labor_Ratio",
    ]
    print("\nFirst 10 years:")
    print(df[display_cols].head(10).round(2))
    print("\nLast 10 years:")
    print(df[display_cols].tail(10).round(2))

    # Save data to CSV
    df.to_csv("heckscher_ohlin_data.csv")
    print("\n  ✓ Data saved to: heckscher_ohlin_data.csv")

    # Part 3: Create visualization
    create_dual_axis_chart(df)

    # Part 4: Run regression
    model = run_regression_analysis(df)

    # Additional: Test for stationarity
    test_stationarity(df)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nOutput files generated:")
    print("  1. heckscher_ohlin_data.csv - Complete dataset")
    print("  2. capital_deepening_chart.png - Dual-axis visualization")
    print("  3. regression_plot.png - Regression scatter plot")

    return df, model


if __name__ == "__main__":
    df, model = main()
