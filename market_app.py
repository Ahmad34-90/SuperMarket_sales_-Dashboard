import pandas as pd 
import plotly.express as px 
import streamlit as st

#------ creating the page configure
st.set_page_config(page_title='SuperMarket_Sales_Dashboard', layout='wide')   

# -----loading the data
df= pd.read_excel('supermarkt_sales.xlsx',header=3)
print(df.columns)
df.columns=df.columns.str.strip()
# --- Heading 
st.markdown("""<center><h1 class="heading1">Super Market Sales Dashboard</h1></center>""", unsafe_allow_html=True)

# Adding KPI
KPI1, KPI2, KPI3 = st.columns(3)

KPI1.markdown('''<div style="
    border: 2px solid #1f77b4; 
    border-radius: 10px; 
    padding: 15px; 
    text-align: center;
    background-color:#f0f8ff;">
<b>Total Sales</b><br>
<span style='font-size:24px;'>${:,.2f}</span><br>
<span style='color:green;'>📈 +5%</span>
</div>'''.format(df['Total'].sum()), unsafe_allow_html=True)
KPI2.markdown("""
<div style="
    border: 2px solid #ff7f0e; 
    border-radius: 10px; 
    padding: 15px; 
    text-align: center;
    background-color:#fffaf0;">
<b>Average Rating</b><br>
<span style='font-size:24px;'>{:.2f}</span><br>
⭐
</div>
""".format(df['Rating'].mean()), unsafe_allow_html=True)

# Total Orders KPI
KPI3.markdown("""
<div style="
    border: 2px solid #2ca02c; 
    border-radius: 10px; 
    padding: 15px; 
    text-align: center;
    background-color:#f0fff0;">
<b>Total Orders</b><br>
<span style='font-size:24px;'>{}</span><br>
🛒
</div>
""".format(len(df)), unsafe_allow_html=True)

st.markdown('---')
_, col1, col2 = st.columns([0.1, 0.45, 0.45])
with col1:
    fig = px.scatter(df, x='Unit price', y='Total', color='Product line',
                    title='Unit Price vs Total by Product Line',
                    labels={'Unit price':'Unit Price ($)', 'Total':'Total Amount ($)'},
                    hover_data=['Quantity','Customer_type','Gender','Payment'])  # shows product line on hover)
    st.plotly_chart(fig)
with col2:
    st.markdown("""
    ### 📝 Insights

    This scatter plot shows the relationship between **Unit Price** and **Total Amount** by **Product Line**.  

    **Key Points:**
    - Higher unit prices generally lead to higher totals.
    - Product lines like **Health and Beauty** and **Electronic Accessories** have higher total sales.
    - Large quantities of lower-priced items can also result in high totals.
    - Hover over points to see Quantity, Customer Type, Gender, and Payment Method.
    """)
    with st.expander("📊 See Detailed Sales Data"):
        st.dataframe(df[['Unit price','Total','Product line']])
    st.download_button("Get Data",
        data=df[['Unit price', 'Total','Product line']].to_csv(index=False).encode('utf-8') ,                
        file_name='supermarket_sales_selected.csv',
        mime='text/csv')

st.markdown('---')
daily_rating =df.groupby(['Date','Product line'])['Rating'].mean().reset_index()
fig = px.line(daily_rating, x='Date', y= 'Rating', color='Product line', markers=True,
              labels={'Rating':'Customer Rating','Date':'Order Day'},
              title='Customer Rating by Date',
              )
st.plotly_chart(fig, use_container_width=True)
