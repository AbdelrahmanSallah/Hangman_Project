import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout='wide', page_title='Banking EDA Dashboard')

html_title = """<h1 style="color:white;text-align:center;">Banking Exploratory Dashboard</h1>"""
st.markdown(html_title, unsafe_allow_html=True)

st.image("https://media.istockphoto.com/photos/bank-building-picture-id640267784?k=6&m=640267784&s=612x612&w=0&h=9MYb9aeNXw7F9h0cSufxCntcT3E9boBGCSZYOIpemjk=",
         use_container_width=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("Data_frame.csv")

# ---------------------------------------------------
# SIDEBAR PAGES
# ---------------------------------------------------
page = st.sidebar.radio(
    "Pages",
    ["Home", "KPIs Dashboard", "Visual Analysis", "Deep Analysis"]
)

# ---------------------------------------------------
# PAGE 1 — HOME
# ---------------------------------------------------
if page == "Home":

    st.subheader("📌 Dataset Overview")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Unique Values Per Column")
    unique_df = pd.DataFrame({
        "Column": df.columns,
        "Unique Values Count": [df[col].nunique() for col in df.columns]
    })
    st.table(unique_df)

    st.subheader("📘 Column Descriptions")
    column_descriptions = {
        "age": "Client age (years).",
        "job": "Type of job.",
        "marital": "Marital status.",
        "education": "Education level.",
        "default": "Has credit default? (yes/no)",
        "balance": "Average yearly balance (EUR).",
        "housing": "Has housing loan? (yes/no)",
        "loan": "Has personal loan? (yes/no)",
        "contact": "Communication type used.",
        "day": "Last contact day of month.",
        "month": "Last contact month.",
        "duration": "Call duration (seconds).",
        "campaign": "Contacts during current campaign.",
        "pdays": "Days since last contact.",
        "previous": "Previous contacts count.",
        "poutcome": "Previous campaign result.",
        "y": "Subscribed to term deposit? (yes/no)",
        "month_contacting_period": "Early/mid/late month.",
        "age_period": "Age group.",
        "high_campaign_pressure": "High campaign pressure (0/1).",
        "contacted_period": "Contact bucket category.",
        "duration_category": "Duration group (short/medium/long)."
    }

    desc_df = pd.DataFrame(list(column_descriptions.items()),
                           columns=["Column Name", "Description"])
    st.table(desc_df)

# ---------------------------------------------------
# PAGE 2 — KPIs DASHBOARD
# ---------------------------------------------------
elif page == "KPIs Dashboard":

    st.subheader("📈 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Clients", f"{len(df):,}")
    col2.metric("Clients Subscribed (y = yes)", df[df['y'] == "yes"].shape[0])
    col3.metric("Subscription Rate (%)",
                round(df[df['y'] == "yes"].shape[0] / len(df) * 100, 2))

    col4, col5, col6 = st.columns(3)
    col4.metric("Average Balance", f"{df['balance'].mean():,.2f}")
    col5.metric("Average Age", f"{df['age'].mean():.1f}")
    col6.metric("Average Duration (sec)", f"{df['duration'].mean():.1f}")


    st.write("---")
    
    # Add unique values section
    st.subheader("📊 Column Unique Values")
    
    # Create a dataframe of unique value counts
    unique_counts = pd.DataFrame({"Column": df.columns,"Unique Values": df.nunique().values,"Data Type": df.dtypes.values}).sort_values("Unique Values", ascending=False)
    
    # Display the table
    st.dataframe(unique_counts, use_container_width=True)
    
# ---------------------------------------------------
# PAGE 3 — VISUAL ANALYSIS
# ---------------------------------------------------
elif page == "Visual Analysis":

    st.subheader("📊 Visual Exploratory Analysis")

    # Histogram Example
    st.write("### Age Distribution")
    st.plotly_chart(px.histogram(df, x="age", nbins=25, title="Age Distribution"),
                    use_container_width=True)

    # Boxplot
    st.write("### Balance by Marital Status")
    st.plotly_chart(px.box(df, x="marital", y="balance",
                           title="Balance vs Marital Status"),
                    use_container_width=True)

    # Bar chart
    st.write("### Job Frequency")
    job_count = df['job'].value_counts().reset_index()
    job_count.columns = ["job", "count"]

    st.plotly_chart(px.bar(job_count, x="job", y="count",
                           title="Job Category Counts"),
                    use_container_width=True)

    # Pie
    st.write("### Loan Distribution")
    st.plotly_chart(px.pie(df, names="loan", title="Loan Status Distribution"),
                    use_container_width=True)

# ---------------------------------------------------
# PAGE 4 — DEEP ANALYSIS
# ---------------------------------------------------
elif page == "Deep Analysis":

    st.subheader("🔍 Deep Insights & Filtering")

    st.write("### Filter by Loan Status")
    loan_filter = st.selectbox("Has Loan?", df['loan'].unique().tolist() + ["All"])

    filtered_df = df.copy()
    if loan_filter != "All":
        filtered_df = filtered_df[filtered_df['loan'] == loan_filter]

    st.dataframe(filtered_df, use_container_width=True)

    st.write("---")

    # Marital Status Filter
    st.write("### Filter by Marital Status")
    marital_filter = st.selectbox("Marital Status", df["marital"].unique().tolist() + ["All"])

    marital_df = df.copy()
    if marital_filter != "All":
        marital_df = marital_df[marital_df["marital"] == marital_filter]

    st.dataframe(marital_df, use_container_width=True)

    st.write("---")

    # Balance Account Filter

    st.write("### Filter by Balance Credit")
    min_balance = df.balance.min()
    max_balance = df.balance.max()

    start_balance, end_balance = st.slider(" Balance range",min_value=min_balance,max_value=max_balance,value=(min_balance, max_balance))

    filtered_df = filtered_df[(filtered_df["balance"] >= start_balance) & (filtered_df["balance"] <= end_balance)]
    st.dataframe(filtered_df, use_container_width=True)

    # Negtive accounts credit
    filter_negative = st.checkbox("Show only negative balances")

    if filter_negative:
        filtered_df = filtered_df[filtered_df["balance"] < 0]
        st.dataframe(filtered_df, use_container_width=True)



    # Subsciption Rate with jobs/ loan status

    st.write("### Subscription Rate by Job & Loan Status")

    df["y_num"] = df["y"].map({"yes": 1, "no": 0})

    job_loan_y = (df.groupby(["job", "loan"])["y_num"].mean().reset_index().rename(columns={"y_num": "subscription_rate"})).sort_values("subscription_rate",ascending=False)

    st.dataframe(job_loan_y)

    st.plotly_chart(px.bar(job_loan_y, x="job", y="subscription_rate", color="loan", title="Subscription Rate by Job & Loan") ,use_container_width=True)

