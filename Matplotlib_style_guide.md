# Matplotlib Corporate Style Guide

## Default Style
plt.style.use("seaborn-v0_8")

## Chart Standards
- figsize=(10, 6) or (12, 6)
- Clear title, x-label, y-label
- Legend when multiple series exist
- Rotate x-axis labels when needed
- Use tight_layout()
- Save charts at 300 DPI

## Preferred Chart Types
- Line charts for trends
- Bar charts for comparisons
- Boxplots/histograms for distributions

## Avoid
- 3D charts
- Pie charts unless explicitly requested
- Bright or unprofessional colors
