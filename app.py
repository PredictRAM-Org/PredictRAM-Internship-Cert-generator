import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime

# Load candidates
candidates_file = 'candidates.xlsx'
candidates_df = pd.read_excel(candidates_file)

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
    if name in candidates_df['Name'].values:
        # Generate PDF Certificate
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'CERTIFICATE OF INTERNSHIP', 0, 1, 'C')
                self.ln(10)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        
        pdf.cell(200, 10, txt = "This is to certify that", ln = True, align = 'C')
        pdf.ln(10)
        pdf.set_font("Arial", 'B', size = 16)
        pdf.cell(200, 10, txt = name, ln = True, align = 'C')
        pdf.ln(10)
        pdf.set_font("Arial", size = 12)
        pdf.cell(200, 10, txt = f"has successfully completed Financial Analyst program from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}.", ln = True, align = 'C')
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Issue Date:", ln = True, align = 'C')
        pdf.cell(200, 10, txt = f"{issue_date.strftime('%d-%m-%Y')}", ln = True, align = 'C')
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Subir Singh", ln = True, align = 'L')
        pdf.cell(200, 10, txt = "Director", ln = True, align = 'L')
        pdf.ln(10)
        pdf.cell(200, 10, txt = "Sheetal Maurya", ln = True, align = 'L')
        pdf.cell(200, 10, txt = "Asst. Prof", ln = True, align = 'L')
        
        pdf_file = f"Internship_Certificate_{name}.pdf"
        pdf.output(pdf_file)
        
        with open(pdf_file, "rb") as file:
            btn = st.download_button(
                label="Download Certificate",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )
    else:
        st.error("Candidate not found in the list.")
