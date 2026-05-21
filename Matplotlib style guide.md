# Matplotlib Corporate Style Guide

## Purpose

This guide defines how the copilot agent must generate all charts. Apply every rule here to every chart produced, unless the user explicitly requests otherwise.

-----

## Required Imports

Always include these at the top of any charting script:

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
```

-----

## Default Style

Always apply the corporate style before any chart is created:

```python
plt.style.use("seaborn-v0_8")
```

> Note: `"seaborn-v0_8"` is the correct style name for matplotlib ≥ 3.6. Do not use the deprecated `"seaborn"` style.

-----

## Chart Standards

Every chart must include all of the following:

|Requirement     |Rule                                                                  |
|----------------|----------------------------------------------------------------------|
|Figure size     |`figsize=(12, 6)` for wide charts, `(10, 6)` for square               |
|Title           |Descriptive, title-cased (e.g., `"Monthly Revenue by Region"`)        |
|X-axis label    |Always present, describes the axis variable                           |
|Y-axis label    |Always present, includes units if applicable (e.g., `"Revenue (USD)"`)|
|Legend          |Required when more than one series is plotted                         |
|X-tick rotation |Rotate 45° whenever labels are dates or long strings                  |
|Layout          |Always call `plt.tight_layout()` before saving                        |
|Save resolution |`dpi=300` for all saved images                                        |
|Close after save|Always call `plt.close()` after saving to free memory                 |

### Standard Chart Template

```python
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots(figsize=(12, 6))

# ... plot data here ...

ax.set_title("Chart Title", fontsize=14)
ax.set_xlabel("X Axis Label")
ax.set_ylabel("Y Axis Label (Units)")
ax.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("chart.png", dpi=300)
plt.close()
```

-----

## Chart Type Selection

|Use Case                                 |Chart Type          |
|-----------------------------------------|--------------------|
|Values over time                         |Line chart          |
|Comparing categories                     |Bar chart           |
|Distributions                            |Histogram or boxplot|
|Part-to-whole (explicitly requested only)|Pie chart           |

### Line Chart Example

```python
# ✅ CORRECT — one line per series, legend included
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots(figsize=(12, 6))

for region, group in report.groupby('region'):
    ax.plot(group['month'].astype(str), group['total_revenue'], label=region, marker='o')

ax.set_title("Monthly Revenue by Region")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (USD)")
ax.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("revenue_by_region.png", dpi=300)
plt.close()
```

### Bar Chart Example

```python
# ✅ CORRECT — grouped bar chart for category comparison
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(report['region'], report['total_revenue'])
ax.set_title("Total Revenue by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Revenue (USD)")
plt.tight_layout()
plt.savefig("revenue_by_region_bar.png", dpi=300)
plt.close()
```

-----

## Patterns to Avoid

|Avoid                                 |Reason                                                       |
|--------------------------------------|-------------------------------------------------------------|
|3D charts                             |Distort data perception; never appropriate for reporting     |
|Pie charts unless explicitly requested|Hard to read; use bar charts for comparisons                 |
|Bright or neon colors                 |Unprofessional; let `seaborn-v0_8` handle the palette        |
|Missing axis labels                   |Charts without labels are uninterpretable                    |
|`plt.show()` in scripts               |Use `plt.savefig()` instead; show is for interactive use only|
|Not calling `plt.close()`             |Memory leak; always close after saving                       |

-----

## Formatting Numbers on Axes

For revenue or large numbers, format y-axis ticks with commas:

```python
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
```