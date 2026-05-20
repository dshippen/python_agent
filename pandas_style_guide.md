# Pandas Style Guide

## General Rules
- Always validate input columns and dtypes.
- Use pd.to_datetime() for date parsing.
- Use pd.to_numeric(errors="coerce") for numeric conversion.
- Treat key columns as non-null.

## Preferred Patterns
- Use assign() for new columns.
- Use pipe() for multi-step transformations.
- Use groupby().agg() with named aggregations.
- Use merge() with explicit join type.
- Use df.loc[] instead of chained indexing.

## Avoid
- inplace=True
- loops (iterrows, itertuples)
- row-wise apply() unless absolutely required

## Output Expectations
- Clean DataFrame
- Explicit dtypes
- Logical column ordering
- Sorted results
