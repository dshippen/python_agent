# Naming Conventions

## Purpose

This guide defines all naming rules the copilot agent must follow when generating variable names, column names, Excel sheet names, and output filenames. Apply these rules to every response without exception.

-----

## Python Variables

- Use `snake_case` for all variable names.
- Names must be descriptive but concise — a reader should understand the variable’s content without seeing its value.
- Avoid single-letter names except for loop counters (`i`, `j`) or lambda parameters (`d`, `x`).

|✅ Correct          |❌ Avoid              |
|-------------------|---------------------|
|`df_clean`         |`df2`, `temp`, `data`|
|`monthly_report`   |`report1`, `rpt`     |
|`revenue_by_region`|`rev`, `r`           |
|`order_count`      |`cnt`, `n`           |
|`df_merged`        |`merged_df_final_v2` |

-----

## DataFrame Column Names

- All column names must be `lowercase_with_underscores`.
- No spaces, camelCase, or title case in column names.
- Be explicit about what the column contains (include units if relevant).

|✅ Correct      |❌ Avoid                         |
|---------------|--------------------------------|
|`order_id`     |`OrderID`, `order id`, `ID`     |
|`order_date`   |`Date`, `orderDate`, `dt`       |
|`total_revenue`|`Revenue`, `totalRevenue`, `rev`|
|`region`       |`Region`, `REGION`              |
|`revenue_usd`  |`revenue_$`                     |

-----

## Excel Sheet Names

Use these standard sheet names. Always apply the appropriate name — do not invent new tab names unless the user requests it.

|Sheet Purpose                  |Name       |
|-------------------------------|-----------|
|Aggregated summary table       |`Summary`  |
|Embedded charts                |`Charts`   |
|Raw or cleaned source data     |`Data`     |
|Category or sub-group breakdown|`Breakdown`|

-----

## Output File Names

- Use descriptive names that include the content type and date.
- Date format: `YYYY_MM` for monthly reports, `QN_YYYY` for quarterly reports.
- Always use the **current date** when generating a filename — do not hardcode a past year.
- Use `snake_case` throughout — no spaces or camelCase in filenames.

### Pattern

```
{content_type}_{period}.xlsx
```

### Examples

|Report Type            |Filename                         |
|-----------------------|---------------------------------|
|Monthly revenue report |`revenue_report_2026_05.xlsx`    |
|Quarterly sales summary|`sales_summary_q2_2026.xlsx`     |
|Regional breakdown     |`regional_breakdown_2026_05.xlsx`|
|Chart image (PNG)      |`revenue_by_region_2026_05.png`  |

### Generating the Date Dynamically in Python

Never hardcode dates in filenames. Always generate them at runtime:

```python
from datetime import date

today = date.today()
# Monthly
filename = f"revenue_report_{today.strftime('%Y_%m')}.xlsx"

# Quarterly
quarter = (today.month - 1) // 3 + 1
filename = f"sales_summary_q{quarter}_{today.year}.xlsx"
```