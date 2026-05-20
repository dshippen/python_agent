# Example reporting workflow

# 1. Clean data
df_clean = (
    df
    .assign(
        date=lambda d: pd.to_datetime(d['date']),
        revenue=lambda d: pd.to_numeric(d['revenue'], errors='coerce'),
        region=lambda d: d['region'].astype('category')
    )
    .dropna(subset=['date', 'revenue'])
)

# 2. Aggregate
report = (
    df_clean
    .assign(month=lambda d: d['date'].dt.to_period('M'))
    .groupby(['month', 'region'], as_index=False)
    .agg(total_revenue=('revenue', 'sum'))
)

# 3. Chart
plt.figure(figsize=(12, 6))
for region, group in report.groupby('region'):
    plt.plot(group['month'].astype(str), group['total_revenue'], label=region)

plt.title("Monthly Revenue by Region")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("chart.png", dpi=300)
plt.close()

# 4. Excel export
wb = Workbook()
ws = wb.active
ws.title = "Summary"

# Write DataFrame
for r in dataframe_to_rows(report, index=False, header=True):
    ws.append(r)

# Format header
for cell in ws[1]:
    cell.font = Font(bold=True)

# Insert chart
img = Image("chart.png")
ws.add_image(img, "H2")

wb.save("Report.xlsx")
