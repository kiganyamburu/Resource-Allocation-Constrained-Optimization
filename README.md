# Resource Allocation & Constrained Optimization

## Heckscher-Ohlin Model Analysis

This project implements an economic analysis based on the **Heckscher-Ohlin (H-O) model**, which predicts that countries export goods that intensively use their abundant factors of production (labor, capital, land, human capital) and import goods that use their scarce factors.

## 📋 Project Overview

The analysis tests the intuition of the H-O model using real U.S. macroeconomic data from FRED (Federal Reserve Economic Data) spanning 1960 to present.

### Key Objectives

- Test the relationship between factor endowments and trade performance
- Analyze the evolution of the U.S. capital-labor ratio over time
- Interpret whether observed trade patterns align with H-O theory
- Critically evaluate the model's assumptions and limitations

## 📁 Project Structure

```
├── heckscher_ohlin_analysis.py   # Main analysis script
├── heckscher_ohlin_data.csv      # Downloaded/generated economic data
├── assignment_answers.md         # Complete analytical answers
├── create_excel_charts.py        # Excel chart generator (openpyxl)
├── create_excel_charts_v2.py     # Excel chart generator (xlsxwriter)
├── convert_to_docx.py            # Script to convert markdown to Word
├── instruction.txt               # Assignment instructions
└── README.md                     # This file
```

## 🔧 Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Install Dependencies

```bash
pip install pandas matplotlib statsmodels numpy
```

For Excel chart generation:

```bash
pip install openpyxl xlsxwriter
```

For Word document conversion:

```bash
pip install python-docx
```

Optional (for FRED API access):

```bash
pip install fredapi pandas-datareader
```

## 🚀 Usage

### Run the Analysis

```bash
python heckscher_ohlin_analysis.py
```

This script will:

1. **Download FRED Data** - Fetches the following series:
   - `GDPC1`: Real GDP (Billions of Chained Dollars)
   - `CLF16OV`: Civilian Labor Force (Thousands of Persons)
   - `GPDIC1`: Real Gross Private Domestic Investment
   - `EXPGSC1`: Real Exports of Goods & Services

2. **Calculate Key Variables**:
   - **Capital Deepening (%)**: Real Investment / Real GDP × 100
   - **Capital-Labor Ratio ($/Worker)**: Real Investment / Labor Force (with unit normalization)

3. **Generate Visualizations** - Creates a dual-axis chart showing both metrics over time

4. **Run Regression Analysis** - Performs OLS regression of Exports vs Capital-Labor Ratio

### Convert to Word Document

```bash
python convert_to_docx.py
```

### Generate Excel Charts

Using openpyxl:

```bash
python create_excel_charts.py
```

Or using xlsxwriter (recommended for better chart formatting):

```bash
python create_excel_charts_v2.py
```

Both scripts create an Excel file with:

- Data sheet with all economic variables
- Dual-axis chart (Capital Deepening vs Capital-Labor Ratio)
- Scatter plot (Real Exports vs Capital-Labor Ratio with trendline)

## 📊 Data Sources

All data is sourced from [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org/):

| Series  | Description                            | Units                            |
| ------- | -------------------------------------- | -------------------------------- |
| GDPC1   | Real Gross Domestic Product            | Billions of Chained 2017 Dollars |
| CLF16OV | Civilian Labor Force                   | Thousands of Persons             |
| GPDIC1  | Real Gross Private Domestic Investment | Billions of Chained 2017 Dollars |
| EXPGSC1 | Real Exports of Goods and Services     | Billions of Chained 2017 Dollars |

## 📈 Key Calculations

### Capital Deepening (Investment % of GDP)

$$\text{Capital Deepening} = \frac{\text{Real Investment}}{\text{Real GDP}} \times 100$$

### Capital-Labor Ratio

$$K/L = \frac{\text{Real Investment (Billions)} \times 10^9}{\text{Labor Force (Thousands)} \times 10^3} = \frac{\text{Investment}}{\text{Workers}}$$

> **Note**: Unit conversion is critical—Investment is in Billions, Labor Force is in Thousands.

## 📝 Analysis Highlights

The complete analysis covers:

- **Regression Critique**: Discussion of unit roots and spurious correlation issues
- **H-O Model Interpretation**: Analysis of U.S. trade patterns in the context of factor endowments
- **Alternative Trade Theories**: Comparison with New Trade Theory and the Gravity Model
- **Policy Implications**: Real-world applications of trade theory

## ⚠️ Important Considerations

1. **Non-Stationarity**: Both exports and K/L ratio contain unit roots, which can lead to spurious regression results
2. **Cointegration**: Consider using Engle-Granger or Johansen tests for proper time-series analysis
3. **Model Limitations**: The H-O model assumes perfect competition, identical technologies, and factor immobility

## 📄 License

This project is for educational purposes as part of an economics assignment on Resource Allocation & Constrained Optimization.

## 🤝 Acknowledgments

- Federal Reserve Bank of St. Louis for FRED data access
- Course instructors for the assignment framework
- Course instructors for the assignment framework
- Course instructors for the assignment framework
- Course instructors for the assignment framework
- Course instructors for the assignment framework
- Course instructors for the assignment framework
