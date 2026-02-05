"""
Create Excel Charts for Heckscher-Ohlin Analysis using xlsxwriter
This script generates an Excel file with proper dual-axis charts
"""

import pandas as pd
import xlsxwriter
import os


def create_excel_with_charts():
    """Create Excel file with data and charts using xlsxwriter"""

    # Load the data
    csv_path = "heckscher_ohlin_data.csv"
    if not os.path.exists(csv_path):
        print(
            f"Error: {csv_path} not found. Please run heckscher_ohlin_analysis.py first."
        )
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded data with {len(df)} rows")

    # Create workbook
    output_file = "heckscher_ohlin_charts.xlsx"
    workbook = xlsxwriter.Workbook(output_file, {"nan_inf_to_errors": True})

    # Formats
    header_format = workbook.add_format(
        {
            "bold": True,
            "font_color": "white",
            "bg_color": "#4472C4",
            "align": "center",
            "border": 1,
        }
    )
    cell_format = workbook.add_format({"border": 1, "num_format": "#,##0.00"})
    percent_format = workbook.add_format({"border": 1, "num_format": "0.00%"})
    year_format = workbook.add_format({"border": 1, "align": "center"})

    # =========================================================================
    # Sheet 1: Data
    # =========================================================================
    ws_data = workbook.add_worksheet("Data")

    headers = [
        "Year",
        "Real_GDP",
        "Labor_Force",
        "Real_Investment",
        "Real_Exports",
        "Capital_Deepening_Pct",
        "Capital_Labor_Ratio",
    ]

    # Write headers
    for col, header in enumerate(headers):
        ws_data.write(0, col, header, header_format)

    # Write data
    for row_idx, row in df.iterrows():
        ws_data.write(row_idx + 1, 0, int(row["Year"]), year_format)
        for col_idx, header in enumerate(headers[1:], 1):
            # Capital Deepening column (index 5) - format as percentage
            if header == "Capital_Deepening_Pct":
                ws_data.write(row_idx + 1, col_idx, row[header] / 100, percent_format)
            else:
                ws_data.write(row_idx + 1, col_idx, row[header], cell_format)

    # Set column widths
    ws_data.set_column("A:A", 8)
    ws_data.set_column("B:G", 18)

    # =========================================================================
    # Sheet 2: Dual-Axis Chart
    # =========================================================================
    ws_chart1 = workbook.add_worksheet("Dual-Axis Chart")

    # Write data for the chart
    ws_chart1.write(0, 0, "Year", header_format)
    ws_chart1.write(0, 1, "Capital Deepening (%)", header_format)
    ws_chart1.write(0, 2, "Capital-Labor Ratio ($)", header_format)

    for row_idx, row in df.iterrows():
        ws_chart1.write(row_idx + 1, 0, int(row["Year"]), year_format)
        # Capital Deepening as percentage (divide by 100 for proper % display)
        ws_chart1.write(
            row_idx + 1, 1, row["Capital_Deepening_Pct"] / 100, percent_format
        )
        ws_chart1.write(row_idx + 1, 2, row["Capital_Labor_Ratio"], cell_format)

    ws_chart1.set_column("A:A", 8)
    ws_chart1.set_column("B:C", 22)

    num_rows = len(df)

    # Create the dual-axis chart
    chart1 = workbook.add_chart({"type": "line"})

    # Add Capital Deepening series (primary Y-axis - left)
    chart1.add_series(
        {
            "name": "Capital Deepening (%)",
            "categories": f"='Dual-Axis Chart'!$A$2:$A${num_rows + 1}",
            "values": f"='Dual-Axis Chart'!$B$2:$B${num_rows + 1}",
            "line": {"color": "#1F77B4", "width": 2.5},
            "marker": {
                "type": "circle",
                "size": 5,
                "fill": {"color": "#1F77B4"},
                "border": {"color": "#1F77B4"},
            },
        }
    )

    # Add K/L Ratio series (secondary Y-axis - right)
    chart1.add_series(
        {
            "name": "K/L Ratio ($)",
            "categories": f"='Dual-Axis Chart'!$A$2:$A${num_rows + 1}",
            "values": f"='Dual-Axis Chart'!$C$2:$C${num_rows + 1}",
            "line": {"color": "#D62728", "width": 2.5},
            "marker": {
                "type": "square",
                "size": 5,
                "fill": {"color": "#D62728"},
                "border": {"color": "#D62728"},
            },
            "y2_axis": True,  # Use secondary Y-axis
        }
    )

    # Configure chart title (with subtitle)
    chart1.set_title(
        {
            "name": "U.S. Capital Deepening and Capital-Labor Ratio (1960-Present)\nHeckscher-Ohlin Model Analysis",
            "name_font": {"bold": True, "size": 14},
        }
    )

    # Configure X-axis
    chart1.set_x_axis(
        {
            "name": "Year",
            "name_font": {"size": 11},
            "num_font": {"size": 9},
            "interval_unit": 5,  # Show every 5th year
            "major_gridlines": {"visible": False},
        }
    )

    # Configure primary Y-axis (left) - Capital Deepening
    chart1.set_y_axis(
        {
            "name": "Capital Deepening (Investment % of GDP)",
            "name_font": {"color": "#1F77B4", "size": 11},
            "num_font": {"color": "#1F77B4"},
            "min": 0.10,
            "max": 0.19,
            "num_format": "0%",
            "major_gridlines": {
                "visible": True,
                "line": {"color": "#D3D3D3", "dash_type": "solid"},
            },
        }
    )

    # Configure secondary Y-axis (right) - K/L Ratio
    chart1.set_y2_axis(
        {
            "name": "Capital-Labor Ratio ($ per Worker)",
            "name_font": {"color": "#D62728", "size": 11},
            "num_font": {"color": "#D62728"},
            "min": 5000,
            "max": 25000,
        }
    )

    # Legend at top left
    chart1.set_legend({"position": "top", "font": {"size": 10}})

    # Chart size
    chart1.set_size({"width": 850, "height": 500})

    # Plot area styling
    chart1.set_plotarea(
        {
            "border": {"color": "#D3D3D3"},
            "fill": {"color": "#FFFFFF"},
        }
    )
    chart1.set_chartarea(
        {
            "fill": {"color": "#FFFFFF"},
        }
    )

    ws_chart1.insert_chart("E2", chart1)

    # =========================================================================
    # Sheet 3: Regression Scatter Plot
    # =========================================================================
    ws_chart2 = workbook.add_worksheet("Regression Plot")

    # Write data for scatter plot
    ws_chart2.write(0, 0, "Capital-Labor Ratio ($)", header_format)
    ws_chart2.write(0, 1, "Real Exports (Billions $)", header_format)

    for row_idx, row in df.iterrows():
        ws_chart2.write(row_idx + 1, 0, row["Capital_Labor_Ratio"], cell_format)
        ws_chart2.write(row_idx + 1, 1, row["Real_Exports"], cell_format)

    ws_chart2.set_column("A:B", 22)

    # Create scatter chart
    scatter_chart = workbook.add_chart({"type": "scatter"})

    scatter_chart.add_series(
        {
            "name": "Observed Data",
            "categories": f"='Regression Plot'!$A$2:$A${num_rows + 1}",
            "values": f"='Regression Plot'!$B$2:$B${num_rows + 1}",
            "marker": {"type": "circle", "size": 6, "fill": {"color": "#1F77B4"}},
            "trendline": {
                "type": "linear",
                "display_equation": True,
                "display_r_squared": True,
                "line": {"color": "red", "width": 2},
            },
        }
    )

    scatter_chart.set_title({"name": "Regression: Real Exports vs Capital-Labor Ratio"})
    scatter_chart.set_x_axis({"name": "Capital-Labor Ratio ($ per Worker)"})
    scatter_chart.set_y_axis({"name": "Real Exports (Billions of Chained $)"})
    scatter_chart.set_legend({"position": "bottom"})
    scatter_chart.set_size({"width": 720, "height": 480})

    ws_chart2.insert_chart("D2", scatter_chart)

    # =========================================================================
    # Sheet 4: Summary Statistics
    # =========================================================================
    ws_summary = workbook.add_worksheet("Summary")

    ws_summary.write(
        0, 0, "Summary Statistics", workbook.add_format({"bold": True, "font_size": 14})
    )

    # Headers
    summary_headers = ["Variable", "Mean", "Std Dev", "Min", "Max"]
    for col, header in enumerate(summary_headers):
        ws_summary.write(2, col, header, header_format)

    # Data
    variables = [
        ("Capital Deepening (%)", "Capital_Deepening_Pct"),
        ("Capital-Labor Ratio ($)", "Capital_Labor_Ratio"),
        ("Real Exports (Billions $)", "Real_Exports"),
        ("Real GDP (Billions $)", "Real_GDP"),
    ]

    for row_idx, (name, col_name) in enumerate(variables, 3):
        ws_summary.write(row_idx, 0, name, cell_format)
        ws_summary.write(row_idx, 1, df[col_name].mean(), cell_format)
        ws_summary.write(row_idx, 2, df[col_name].std(), cell_format)
        ws_summary.write(row_idx, 3, df[col_name].min(), cell_format)
        ws_summary.write(row_idx, 4, df[col_name].max(), cell_format)

    ws_summary.set_column("A:A", 25)
    ws_summary.set_column("B:E", 15)

    # Close workbook
    workbook.close()

    print(f"\n✓ Excel file saved: {output_file}")
    print("\nSheets created:")
    print("  1. Data - Complete dataset")
    print(
        "  2. Dual-Axis Chart - Capital Deepening vs K/L Ratio (with years on X-axis)"
    )
    print("  3. Regression Plot - Real Exports vs K/L Ratio with trendline")
    print("  4. Summary - Summary statistics")

    return output_file


if __name__ == "__main__":
    create_excel_with_charts()
