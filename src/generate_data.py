import os
import random
import datetime
import pandas as pd
from faker import Faker

fake = Faker()

def execute_generation(project_root):
    regions = ['Southern Region (POM)', 'Momase Region (Lae)']
    plans = ['prepaid basic', 'PREPAID PREMIUM', 'Postpaid Unlimited', 'postpaid family']
    payment_methods = ['Credit Card', 'Mobile Wallet', 'Bank Transfer', 'Cash']
    
    num_records = random.randint(300, 500)  # Increased slightly to give a healthy distribution across months
    new_rows = []
    
    for _ in range(num_records):
        # --- FIX: Distribute dates across months 1 to 10 in the year 2026 ---
        random_month = random.randint(1, 10)
        random_day = random.randint(1, 28)  # Safe limit for all calendar months
        invoice_date_obj = datetime.date(2026, random_month, random_day)
        target_date_str = invoice_date_obj.strftime("%Y-%m-%d")

        if random.random() > 0.02:
            invoice_id = f"INV-2026-{random.randint(100000, 999999)}"
        else:
            invoice_id = None
            
        customer_id = f"CUST-{random.randint(1000, 9999)}" if random.random() > 0.05 else None
        customer_name = fake.name() if customer_id else None
        customer_email = fake.email() if customer_id else None
        customer_phone = fake.phone_number()
        region = random.choice(regions) if random.random() > 0.05 else None
        store_address = fake.address().replace('\n', ', ')
        plan_type = random.choice(plans)
        
        monthly_charges = round(random.uniform(29.99, 119.99), 2)
        extra_fees = round(random.choice([0.0, 0.0, 15.50]), 2)
        total_invoice_amount = round(monthly_charges + extra_fees, 2)
        payment_status = random.choice(['paid', 'PAID', 'pending', 'OVERDUE', None])
        payment_method = random.choice(payment_methods)
        
        new_rows.append([
            invoice_id, target_date_str, customer_id, customer_name, customer_email, 
            customer_phone, region, store_address, plan_type, 100, 12, 
            monthly_charges, extra_fees, total_invoice_amount, payment_status, payment_method
        ])
        
    columns = [
        "invoice_id", "invoice_date", "customer_id", "customer_name", "customer_email", 
        "customer_phone", "region", "store_address", "plan_type", "data_allowance_gb", 
        "contract_months", "monthly_charges", "extra_fees", "total_invoice_amount", 
        "payment_status", "payment_method"
    ]
    
    daily_df = pd.DataFrame(new_rows, columns=columns)
    master_raw_path = os.path.join(project_root, "data", "raw", "master_raw_traffic.csv")
    
    file_exists = os.path.exists(master_raw_path)
    daily_df.to_csv(master_raw_path, mode='a', index=False, header=not file_exists)
    print(f"[GENERATOR] Appended {num_records} distributed rows into master log across 2026.")

if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    execute_generation(root)
