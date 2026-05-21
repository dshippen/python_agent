# Reporting Workflow Example
#
# Purpose: This file is the canonical end-to-end reporting workflow.
# The copilot agent must use this as the reference pattern when generating
# reporting scripts. Every step here reflects the pandas, matplotlib,
# openpyxl, and naming convention style guides.
#
# This script is fully self-contained and runnable.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import date
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# 0. Style definitions (define once, reuse throughout)
# ---------------------------------------------------------------------------
header_font = Font(bold=True, size=11)
header_fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
thin_side = Side(border_style="thin", color="000000")
thin_border = Border(top=thin_side, left=thin_side, right=thin_side, bottom=thin_side)
center_align = Alignment(horizontal="center", vertical="center")
currency_format = "$#,##0.00"


def autofit_columns(ws, min_width=10, max_width=40):
    """Set column widths based on content length."""
    for col in ws.columns:
        max_len = max(
            len(str(cell.value)) if cell.value is not None else 0
            for cell in col
        )
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 2, min_width), max_width)


# ---------------------------------------------------------------------------
# 1. Validate input
# ---------------------------------------------------------------------------
# Replace `df` with your actual DataFrame source (CSV load, DB query, etc.)
# Example: df = pd.read_csv("orders.csv")

required_cols = ['order_date', 'revenue', 'region', 'order_id']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# ---------------------------------------------------------------------------
# 2. Clean data
# ---------------------------------------------------------------------------
df_clean = (
    df
    .assign(
        order_date=lambda d: pd.to_datetime(d['order_date']),
        revenue=lambda d: pd.to_numeric(d['revenue'], errors='coerce'),
        region=lambda d: d['region'].astype('category')
    )
    .dropna(subset=['order_date', 'revenue'])
)

# ---------------------------------------------------------------------------
# 3. Aggregate
# ---------------------------------------------------------------------------
report = (
    df_clean
    .assign(month=lambda d: d['order_date'].dt.to_period('M'))
    .groupby(['month', 'region'], as_index=False)
    .agg(
        total_revenue=('revenue', 'sum'),
        order_count=('order_id', 'count')
    )
    .sort_values(['month', 'region'])
)

# ---------------------------------------------------------------------------
# 4. Chart — line chart of monthly revenue by region
# ---------------------------------------------------------------------------
chart_path = "revenue_by_region.png"

plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots(figsize=(12, 6))

for region, group in report.groupby('region'):
    ax.plot(
        group['month'].astype(str),
        group['total_revenue'],
        label=region,
        marker='o'
    )

ax.set_title("Monthly Revenue by Region", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(chart_path, dpi=300)
plt.close()

# ---------------------------------------------------------------------------
# 5. Excel export
# ---------------------------------------------------------------------------
wb = Workbook()
ws = wb.active
ws.title = "Summary"

# Write data
for row in dataframe_to_rows(report, index=False, header=True):
    ws.append(row)

# Format header row
for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = center_align

# Format revenue column (column 3) as currency
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=3, max_col=3):
    for cell in row:
        cell.number_format = currency_format

# Auto-fit column widths
autofit_columns(ws)

# Embed chart image
img = Image(chart_path)
img.anchor = "H2"
ws.add_image(img)

# ---------------------------------------------------------------------------
# 6. Save with dynamic filename
# ---------------------------------------------------------------------------
today = date.today()
output_path = f"revenue_report_{today.strftime('%Y_%m')}.xlsx"
wb.save(output_path)
print(f"Report saved: {output_path}")
