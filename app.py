import streamlit as st
import pandas as pd
from fpdf import FPDF

# Load candidates
candidates_file = 'candidates.xlsx'  # Update this path as necessary
candidates_df = pd.read_excel(candidates_file)

# Debugging: Display columns in the dataframe
st.write("Columns in the candidates file:", candidates_df.columns.tolist())

# Check for leading/trailing spaces in column names
candidates_df.columns = candidates_df.columns.str.strip()

# Function to generate certificate
def generate_certificate(name, start_date, end_date, issue_date):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 24)
            self.set_text_color(30, 144, 255)  # Color similar to the sample
            self.cell(0, 10, 'CERTIFICATE OF INTERNSHIP', 0, 1, 'C')
            self.ln(20)

        def footer(self):
            self.set_y(-30)
            self.set_font('Arial', 'I', 12)
            self.cell(0, 10, 'Subir Singh', 0, 1, 'L')
            self.cell(0, 10, 'Director', 0, 1, 'L')
            self.ln(10)
            self.cell(0, 10, 'Sheetal Maurya', 0, 1, 'L')
            self.cell(0, 10, 'Asst. Prof', 0, 1, 'L')

    pdf = PDF()
    pdf.add_page()
    
    # Add Images (placeholders for now)
    pdf.image('logo.png', 10, 10, 30)  # Replace with actual path
    pdf.image('another_logo.png', 170, 10, 30)  # Replace with actual path
    
    pdf.set_font("Arial", size=12)
    pdf.ln(30)
    pdf.cell(0, 10, "The certificate is proudly presented to", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, name, 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"for successfully completing Financial Analyst program from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}.", 0, 1, 'C')
    pdf.ln(10)
    
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
    # Ensure the 'Candidate Name' column is present in the dataframe
    st.write("Checking for 'Candidate Name' column...")
    if 'Candidate Name' in candidates_df.columns:
        st.write("'Candidate Name' column found.")
        if name in candidates_df['Candidate Name'].values:
            st.write("Candidate found in the list.")
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
