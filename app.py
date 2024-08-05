import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load candidates
candidates_file = 'candidates.xlsx'  # Update this path as necessary
candidates_df = pd.read_excel(candidates_file)

# Check for leading/trailing spaces in column names
candidates_df.columns = candidates_df.columns.str.strip()

# Function to generate certificate
def generate_certificate(name, start_date, end_date, issue_date):
    class PDF(FPDF):
        def header(self):
            # Add logos at the top center
            self.image('image.png', 50, 10, 100)  # Adjust the path and size as necessary
            self.ln(35)
            self.set_font('Arial', 'B', 24)
            self.set_text_color(0, 0, 128)  # Navy blue color
            self.cell(0, 10, 'CERTIFICATE OF INTERNSHIP', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            # Footer with images and names
            self.set_y(-60)
            self.image('signature1.png', 10, self.get_y(), 30)  # Replace with actual path
            self.image('signature2.png', 170, self.get_y(), 30)  # Replace with actual path
            self.set_font('Arial', 'I', 12)
            self.cell(0, 10, 'Sheetal Maurya', 0, 1, 'L')
            self.cell(0, 10, 'Asst. Prof', 0, 1, 'L')
            self.set_x(-80)
            self.cell(0, 10, 'Subir Singh', 0, 1, 'R')
            self.set_x(-80)
            self.cell(0, 10, 'Director', 0, 1, 'R')
            self.set_y(-30)
            self.image('footer_image.png', 60, self.get_y(), 80)  # Replace with actual path

        def add_border(self):
            self.set_line_width(2.0)
            self.set_draw_color(0, 0, 128)  # Navy blue color
            self.rect(10, 10, self.w - 20, self.h - 20)
            self.set_line_width(1.0)
            self.set_draw_color(255, 140, 0)  # Orange color
            self.rect(12, 12, self.w - 24, self.h - 24)

    pdf = PDF()
    pdf.add_page()

    # Add border
    pdf.add_border()

    pdf.set_font("Arial", size=12)
    pdf.ln(50)
    pdf.cell(0, 10, "Financial Analyst Internship", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "This certifies that", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, name, 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"has successfully completed the Financial Analyst Internship program at PredictRAM", 0, 1, 'C')
    pdf.cell(0, 10, f"from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}.", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.cell(0, 10, "Key Responsibilities and Achievements:", 0, 1, 'L')
    pdf.ln(5)
    pdf.cell(0, 10, "• Conducted in-depth fundamental and technical analysis of stocks.", 0, 1, 'L')
    pdf.cell(0, 10, "• Tracked and recorded market data, preparing forecasts on financial and economic events.", 0, 1, 'L')
    pdf.cell(0, 10, "• Provided insights on upcoming economic events and trends.", 0, 1, 'L')
    pdf.cell(0, 10, "• Mastered advanced software for predictive analysis.", 0, 1, 'L')
    pdf.cell(0, 10, "• Developed research reports on national economic conditions and financial forecasts.", 0, 1, 'L')
    pdf.cell(0, 10, "• Contributed to secondary financial research, enhancing team outputs.", 0, 1, 'L')
    pdf.ln(10)
    
    pdf.cell(0, 10, "Performance Summary:", 0, 1, 'L')
    pdf.ln(5)
    pdf.cell(0, 10, f"{name} demonstrated strong analytical skills, effectively contributed to team projects,", 0, 1, 'L')
    pdf.cell(0, 10, "and delivered valuable insights that supported the company’s objectives.", 0, 1, 'L')
    pdf.ln(20)
    
    pdf.cell(0, 10, f"Issue Date: {issue_date.strftime('%d-%m-%Y')}", 0, 1, 'C')
    pdf.ln(20)

    pdf_file = f"Internship_Certificate_{name}.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Streamlit App
st.title("Internship Certificate Generator")

# Input Form
st.header("Enter Internship Details")

with st.form("internship_form"):
    name = st.text_input("Candidate Name")
    start_date = st.date_input("Internship Start Date")
    end_date = st.date_input("Internship End Date")
    issue_date = st.date_input("Issue Date")
    submit_button = st.form_submit_button(label="Generate Certificate")

# Check if the candidate is in the list
if submit_button:
    if 'Candidate Name' in candidates_df.columns:
        if name in candidates_df['Candidate Name'].values:
            # Generate PDF Certificate
            pdf_file = generate_certificate(name, start_date, end_date, issue_date)
            
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Download Certificate",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
        else:
            st.error("Candidate not found in the list.")
    else:
        st.error("'Candidate Name' column not found in the candidates file.")
