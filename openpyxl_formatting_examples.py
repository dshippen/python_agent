from openpyxl.styles import Font, PatternFill, Border, Side

# Header style
header_font = Font(bold=True)
header_fill = PatternFill(start_color="DDDDDD", fill_type="solid")

# Thin border
thin = Side(border_style="thin", color="000000")
thin_border = Border(top=thin, left=thin, right=thin, bottom=thin)

# Number formats
currency_format = "$#,##0.00"
percent_format = "0.0%"
date_format = "yyyy-mm-dd"

# Example usage:
# cell.font = header_font
# cell.fill = header_fill
# cell.border = thin_border
# cell.number_format = currency_format
