import os
import pandas as pd

def run_etl_pipeline():
    # 1. Setup Base File Directory Systems
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw", "master_raw_traffic.csv")
    processed_dir = os.path.join(base_dir, "data", "processed")
    processed_path = os.path.join(processed_dir, "clean_invoices.csv")
    
    print("[PIPELINE] Initializing ETL job iteration script...")
    
    if not os.path.exists(raw_path):
        print(f"[ERROR] Raw source tracking log file not found at: {raw_path}")
        return

    # 2. Extract Data
    df = pd.read_csv(raw_path)
    initial_row_count = len(df)
    
    # 3. Transform Data (Cleaning & Quality Standardizations)
    # Remove records missing crucial tracking IDs (Quarantine Rule)
    df = df.dropna(subset=['invoice_id'])
    cleansed_row_count = len(df)
    
    # Standardize data text string layouts to avoid fragmented metrics
    if 'plan_type' in df.columns:
        df['plan_type'] = df['plan_type'].str.upper().str.strip()
        
    if 'payment_status' in df.columns:
        df['payment_status'] = df['payment_status'].str.upper().str.strip()
        df['payment_status'] = df['payment_status'].fillna("UNKNOWN")
        
    if 'region' in df.columns:
        df['region'] = df['region'].fillna("UNKNOWN REGION")

    # 4. Load Data (Save the optimized layer out)
    os.makedirs(processed_dir, exist_ok=True)
    df.to_csv(processed_path, index=False)
    
    print(f"[PIPELINE] Processing Phase Completed.")
    print(f" -> Initial Records Extracted: {initial_row_count}")
    print(f" -> Dropped Anomaly Rows: {initial_row_count - cleansed_row_count}")
    print(f" -> Loaded Target Clean Outpost: {processed_path}")

if __name__ == "__main__":
    run_etl_pipeline()
