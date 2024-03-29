import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Adidas",page_icon="👟", layout="wide")
# Reading the data from the Excel file
df = pd.read_excel("Adidas.xlsx")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('adidas-logo.jpg')

# Creating a visually appealing header
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)

html_title = """
    <style>
    .title-test {
        font-family: 'Montserrat', sans-serif;
        font-weight: bold;
        padding: 10px;
        border-radius: 10px;
        background-color: #e3f2fd;
        color: #0077b6;
    }
    </style>
    <center><h1 class="title-test">Adidas Interactive Sales Dashboard 📊</h1></center>
"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# Adding a creative touch to the date display
col3, col4, col5 = st.columns([0.1, 0.45, 0.45])
with col3:
    box_date = datetime.datetime.now().strftime("%d %B %Y")
    st.write(f"📅 Last updated on: {box_date}")

# Interactive data visualization with hover data
with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales": "Total Sales ($)"},
                 title="Total Sales by Retailer 🏪", hover_data=["TotalSales"],
                 template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

# Expander and download button sections with creative emojis
_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander("👀 Retailer-wise Sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("📥 Get Data", data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by=df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x="Month_Year", y="TotalSales", title="Total Sales Over Time 📈",
                   template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("📆 Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button("📥 Get Data", data=result.to_csv().encode("utf-8"),
                       file_name="Monthly Sales.csv", mime="text/csv")

st.divider()

result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# Dual-axis chart for total sales and units sold
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"], y=result1["TotalSales"], name="Total Sales ($)"))
fig3.add_trace(go.Scatter(x=result1["State"], y=result1["UnitsSold"], mode="lines",
                          name="Units Sold 📦", yaxis="y2"))
fig3.update_layout(
    title="Total Sales and Units Sold by State 🏦",
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales ($)", showgrid=False),
    yaxis2=dict(title="Units Sold", overlaying="y", side="right"),
    template="gridon",
    legend=dict(x=1, y=1.1)
)
_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("📊 View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("📥 Get Data", data=result1.to_csv().encode("utf-8"),
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")
st.divider()

_, col7 = st.columns([0.1, 1])
treemap = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path=["Region", "City"], values="TotalSales",
                  hover_name="TotalSales (Formatted)",
                  hover_data=["TotalSales (Formatted)"],
                  color="City", height=700, width=600)
fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader("🌍 Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])
with view4:
    result2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum()
    expander = st.expander("📖 View data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button("📥 Get Data", data=result2.to_csv().encode("utf-8"),
                       file_name="Sales_by_Region.csv", mime="text.csv")

_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])
with view5:
    expander = st.expander("📄 View Sales Raw Data")
    expander.write(df)
with dwn5:
    st.download_button("📥 Get Raw Data", data=df.to_csv().encode("utf-8"),
                       file_name="SalesRawData.csv", mime="text/csv")
st.divider()