import fpdf

def create_financial_report(title, data):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, title, ln=True, align="C")
    for key, value in data.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)
    pdf.output(f"{title}.pdf")

# Example usage:
financial_data = {"Revenue": "$10M", "Profit Margin": "15%", "Projected Growth": "12%"}
create_financial_report("Q4 Financial Report", financial_data)