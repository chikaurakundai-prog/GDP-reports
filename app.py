import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from io import BytesIO
import base64

st.set_page_config(page_title="Procurement Reports", layout="wide")
st.title("🌐 Kundai Chikaura Procurement GT Monthly Reports")

# Sidebar month selector for previous reports
months = ["Dec 2025", "Nov 2025", "Oct 2025"]
selected_month = st.sidebar.selectbox("Select Month", months)
st.sidebar.info("Update data via GitHub push for auto-refresh.")

# Tabs for interactivity
tab1, tab2, tab3 = st.tabs(["📝 Duties Summary", "📊 KPIs Dashboard", "🖼️ Media & PDF"])

with tab1:
    st.header(f"{selected_month} Activities")
    st.markdown("""
    - Investigated foreign imports and tariff codes.
    - Mitigated wastes: customs delays, overstocking (saved $X).
    - Tracked duties paid via integrated system.
    """)  # Add your text summaries
    st.image("images/process_map.png", caption="Procurement Flow")  # Your images

with tab2:
    @st.cache_data
    def load_data(month):
        return pd.read_csv(f"data/{month.lower()}.csv")  # e.g., columns: Supplier, OTIF, Savings
    df = load_data(selected_month)
    fig = px.bar(df, x="Supplier", y="Savings USD", color="OTIF %", title="Performance")
    st.plotly_chart(fig, use_container_width=True)
    col1, col2 = st.columns(2)
    col1.metric("Total Savings", df["Savings USD"].sum())
    col2.metric("Avg Cycle Time", f"{df['Cycle Days'].mean():.1f} days")

with tab3:
    st.video("videos/demo.mp4")  # Your videos
    if st.button("📥 Download PDF Report"):
        pdf_bytes = generate_pdf(df, selected_month)
        st.download_button("Download", pdf_bytes, f"{selected_month}_report.pdf", "application/pdf")

def generate_pdf(df, month):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Procurement Report: {month}", ln=1, align="C")
    # Add table, images, etc.
    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    return pdf_output.getvalue()
