import os
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Telecom Edge Data Warehouse",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Telecom Edge Data Warehouse Dashboard")
st.markdown("Broadcasting processed data pipelines straight from your lab server environment.")

# 2. Locate our target directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(BASE_DIR, "data", "processed")

if not os.path.exists(TARGET_DIR):
    st.error(f"Target directory not found: `{TARGET_DIR}`. Please run your data pipeline first.")
else:
    files = [f for f in os.listdir(TARGET_DIR) if f.endswith(('.csv', '.json', '.parquet'))]
    
    if not files:
        st.warning(f"No processed data files found inside `{TARGET_DIR}`.")
    else:
        st.sidebar.header("📁 Data Source Selection")
        selected_file = st.sidebar.selectbox("Choose a dataset to inspect:", files)
        file_path = os.path.join(TARGET_DIR, selected_file)
        
        try:
            if selected_file.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif selected_file.endswith('.json'):
                df = pd.read_json(file_path)
            elif selected_file.endswith('.parquet'):
                df = pd.read_parquet(file_path)
                
            st.subheader(f"📋 Inspecting: {selected_file}")
            
            invoice_col = "total_invoice_amount"
            region_col = "region"
            plan_col = "plan_type"
            date_col = "invoice_date"
            status_col = "payment_status"

            available_cols = df.columns.tolist()

            # ---- CARD CHART ----
            st.markdown("### 🏷️ Key Executive Metrics")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            if invoice_col in available_cols:
                total_invoice_sum = df[invoice_col].sum()
                metric_col1.metric("Sum of Total Invoice", f"\${total_invoice_sum:,.2f}")
            else:
                metric_col1.metric("Sum of Total Invoice", "Column Not Found")
                
            metric_col2.metric("Total Records Rows", f"{df.shape[0]:,}")
            metric_col3.metric("Total Attributes Columns", f"{df.shape[1]}")
            
            st.markdown("---")
            st.markdown("### 🔍 Live Data Table Viewer")
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📊 Power BI Ported Visualizations")
            
            row1_col1, row1_col2 = st.columns(2)
            row2_col1, row2_col2 = st.columns(2)
            
            # ---- DONUT CHART ----
            with row1_col1:
                st.subheader("🍩 Total Invoice distribution by Region")
                if invoice_col in available_cols and region_col in available_cols:
                    fig_donut = px.pie(df, names=region_col, values=invoice_col, hole=0.4)
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:
                    st.info(f"Requires '{region_col}' and '{invoice_col}' fields.")

            # ---- STACKED BAR CHART ----
            with row1_col2:
                st.subheader("📊 Plan Type Invoice Analysis")
                if invoice_col in available_cols and plan_col in available_cols:
                    df_bar = df.groupby(plan_col, as_index=False)[invoice_col].sum()
                    fig_bar = px.bar(df_bar, y=plan_col, x=invoice_col, orientation='h')
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info(f"Requires '{plan_col}' and '{invoice_col}' fields.")

            # ---- FIXED LINE CHART: MONTHLY TRENDS ----
            with row2_col1:
                st.subheader("📈 Invoicing Trends Over Time (2026)")
                if invoice_col in available_cols and date_col in available_cols:
                    df_line_clean = df.copy()
                    df_line_clean[date_col] = pd.to_datetime(df_line_clean[date_col])
                    
                    # Extract Month Period and Name
                    df_line_clean['Month_Num'] = df_line_clean[date_col].dt.month
                    df_line_clean['Month'] = df_line_clean[date_col].dt.strftime('%B')
                    
                    group_cols = ['Month_Num', 'Month']
                    if status_col in available_cols:
                        group_cols.append(status_col)
                        
                    # Aggregate and sort sequentially by calendar month number
                    df_line = df_line_clean.groupby(group_cols, as_index=False)[invoice_col].sum()
                    df_line = df_line.sort_values(by='Month_Num')
                    
                    fig_line = px.line(
                        df_line, 
                        x='Month', 
                        y=invoice_col, 
                        color=status_col if status_col in available_cols else None,
                        title="Revenue Performance Trend by Month (2026)",
                        markers=True  # Adds visual points onto line intersections
                    )
                    st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.info(f"Requires '{date_col}' and '{invoice_col}' fields.")
                    
            with row2_col2:
                st.subheader("💡 System Architecture Logging")
                st.caption("File Metrics Profile:")
                st.text(f"Source Directory Path: {file_path}")
                st.text(f"Allocated Disk Size: {os.path.getsize(file_path) / 1024:.2f} KB")

        except Exception as e:
            st.error(f"Error compiling visual layers: {e}")
