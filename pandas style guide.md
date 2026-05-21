# Pandas Style Guide

## Purpose

This guide defines how the copilot agent must write all pandas code. Rules here are not suggestions — apply them to every generated snippet, transformation, and export.

-----

## Required Imports

Always include these at the top of any pandas script:

```python
import pandas as pd
import numpy as np
```

-----

## Input Validation

Always validate input columns and data types before any transformation.

```python
# ✅ CORRECT — validate before use
required_cols = ['order_date', 'revenue', 'region']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")
```

- Use `pd.to_datetime()` for all date columns — never assume a column is already a datetime.
- Use `pd.to_numeric(errors="coerce")` for numeric columns — this converts bad values to NaN instead of raising.
- Treat key columns (`order_id`, `order_date`, `revenue`) as non-null; drop rows where they are missing.

-----

## Preferred Patterns

### Use `assign()` for New Columns

```python
# ✅ CORRECT
df_clean = df.assign(
    order_date=lambda d: pd.to_datetime(d['order_date']),
    revenue=lambda d: pd.to_numeric(d['revenue'], errors='coerce'),
    region=lambda d: d['region'].astype('category')
)

# ❌ WRONG — chained assignment, unpredictable behavior
df['order_date'] = pd.to_datetime(df['order_date'])
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
```

### Use `pipe()` for Multi-Step Transformations

```python
# ✅ CORRECT — readable pipeline
def clean_dates(df):
    return df.assign(order_date=lambda d: pd.to_datetime(d['order_date']))

def drop_nulls(df):
    return df.dropna(subset=['order_date', 'revenue'])

df_clean = df.pipe(clean_dates).pipe(drop_nulls)
```

### Use `groupby().agg()` with Named Aggregations

```python
# ✅ CORRECT — named aggregations are explicit and readable
report = (
    df_clean
    .groupby(['month', 'region'], as_index=False)
    .agg(
        total_revenue=('revenue', 'sum'),
        order_count=('order_id', 'count'),
        avg_revenue=('revenue', 'mean')
    )
)

# ❌ WRONG — unnamed aggregations require guessing column names downstream
df.groupby('region')['revenue'].sum()
```

### Use `merge()` with Explicit Join Type

```python
# ✅ CORRECT — always name the join type
df_merged = df_orders.merge(df_customers, on='customer_id', how='left')

# ❌ WRONG — implicit inner join hides intent
df_orders.merge(df_customers, on='customer_id')
```

### Use `df.loc[]` for Indexing

```python
# ✅ CORRECT
df.loc[df['region'] == 'North', 'revenue']

# ❌ WRONG — chained indexing causes SettingWithCopyWarning
df[df['region'] == 'North']['revenue']
```

-----

## Patterns to Avoid

|Avoid                          |Use Instead                            |Reason                                                       |
|-------------------------------|---------------------------------------|-------------------------------------------------------------|
|`inplace=True`                 |Reassign the variable                  |Inplace mutations are hard to debug and chain                |
|`iterrows()` / `itertuples()`  |`assign()`, `groupby()`, vectorized ops|Loops are slow and unreadable                                |
|Row-wise `apply()`             |Vectorized operations                  |Apply is slow; use only when no vectorized alternative exists|
|Chained indexing `df[...][...]`|`df.loc[...]`                          |Chained indexing produces unpredictable copies vs views      |

-----

## Output Expectations

Every DataFrame produced by the agent must:

- Have explicit, correct dtypes (dates as `datetime64`, numbers as `float64` or `int64`, categoricals as `category`).
- Have columns named in `lowercase_with_underscores` (see naming conventions).
- Be sorted in a logical order (e.g., by date, then region).
- Contain no unnamed columns (no `Unnamed: 0` from CSV artifacts).
- Have nulls either dropped or filled — never silently passed downstream.

-----

## Complete Example

```python
import pandas as pd

# Validate
required_cols = ['order_date', 'revenue', 'region', 'order_id']
missing = [c for c in required_cols if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Clean
df_clean = (
    df
    .assign(
        order_date=lambda d: pd.to_datetime(d['order_date']),
        revenue=lambda d: pd.to_numeric(d['revenue'], errors='coerce'),
        region=lambda d: d['region'].astype('category')
    )
    .dropna(subset=['order_date', 'revenue'])
)

# Aggregate
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
```