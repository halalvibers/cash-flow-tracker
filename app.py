import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Business Cash Flow Tracker", page_icon="💰", layout="wide"
)

# Custom Professional UI Styling (CSS)
st.markdown(
    """
    <style>
    /* Main background color */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Metric cards styling */
    [data-testid="stMetric"] {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }

    /* Success / Info boxes */
    .stAlert {
        border-radius: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📊 Business & Expense Cash Flow Tracker")
st.write(
    "Manage your income, track business expenses, and visualize your cash flow instantly."
)

# Initialize session state to store transactions
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(
        columns=["Date", "Type", "Category", "Amount", "Description"]
    )

# Sidebar for Inputting New Transactions
st.sidebar.header("➕ Add New Transaction")

with st.sidebar.form("transaction_form", clear_on_submit=True):
    t_date = st.date_input("Date")
    t_type = st.selectbox("Type", ["Income", "Expense"])
    t_category = st.selectbox(
        "Category",
        [
            "Sales/Revenue",
            "Raw Materials",
            "Equipment",
            "Marketing",
            "Utilities",
            "Other",
        ],
    )
    t_amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    t_desc = st.text_input("Description / Notes")

    submit_button = st.form_submit_button(label="Add Transaction")

    if submit_button:
        if t_amount > 0:
            new_data = pd.DataFrame(
                [[t_date, t_type, t_category, t_amount, t_desc]],
                columns=["Date", "Type", "Category", "Amount", "Description"],
            )
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_data], ignore_index=True
            )
            st.sidebar.success("Transaction added successfully!")
        else:
            st.sidebar.error("Please enter an amount greater than 0.")

# Main Dashboard Metrics
df = st.session_state.transactions

if not df.empty:
    # Calculate Metrics
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    net_profit = total_income - total_expense

    # Display Metrics in Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expense:,.2f}")
    col3.metric(
        "Net Cash Flow",
        f"${net_profit:,.2f}",
        delta=f"${net_profit:,.2f}",
    )

    st.markdown("---")

    # Visual Charts Section
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📈 Income vs Expenses")
        type_summary = df.groupby("Type")["Amount"].sum()
        st.bar_chart(type_summary)

    with chart_col2:
        st.subheader("📊 Spending by Category")
        if not df[df["Type"] == "Expense"].empty:
            cat_expense = (
                df[df["Type"] == "Expense"]
                .groupby("Category")["Amount"]
                .sum()
            )
            st.bar_chart(cat_expense)
        else:
            st.info("Add some expenses to see category breakdowns.")

    st.markdown("---")

# Display Data Table and Delete Option
st.subheader("📋 Recent Transactions")
if not df.empty:
    st.dataframe(df, use_container_width=True)

    # Delete Section
    st.write("### 🗑️ Delete a Transaction")
    row_to_delete = st.number_input(
        "Enter the Row Index number to delete",
        min_value=0,
        max_value=len(df) - 1,
        step=1,
    )
    if st.button("Delete Selected Row"):
        st.session_state.transactions = (
            st.session_state.transactions.drop(row_to_delete)
            .reset_index(drop=True)
        )
        st.success(f"Row {row_to_delete} deleted successfully!")
        st.rerun()
else:
    st.info("No transactions added yet. Use the sidebar to add your first one!")