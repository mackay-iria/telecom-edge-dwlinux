# Local Telecom Data Warehouse Project (`telecom-edge-dw`)

Hi, I'm Mackay. This is a personal practice project I built to learn how data moves from a messy operational state into clean relational models for a real-time web application, mimicking enterprise data pipelines using local tools and cross-OS infrastructure.

## My Profile & Goals
* **About Me:** Graduate Support Officer at Datec PNG Limited (Pronto Xi ERP Systems Support).
* **Education:** B.Sc. in Mathematics, Statistics, and Computer Science.
* **Why I Built This:** To transition into Data Engineering or Database Architecture. I am a recent graduate who is eager to learn from experienced professionals, contribute to a team, and make data engineering, analytics, and dashboards simpler. 
* **My Learning Journey:** While I haven't yet fully mastered advanced SQL or data infrastructure engineering, I am building my skills bit-by-bit through hands-on practice—creating data pipelines, testing queries, and processing information using Python, interactive scripts, and core packages like `pandas`, `plotly`, and `faker`.

---

## Skills I Am Actively Mastering
* **Cross-OS Administration:** Working comfortably across standard client environments (Windows Desktop with Pronto Xi v740 Thin Clients) and backend runtime environments (Ubuntu Server VMs via SSH over custom ports).
* **Linux CLI & Systems Networking:** Managing daemon services (`sshd`), manipulating firewalls (`ufw`), auditing listening network sockets (`ss -tulpn`), and organizing package environments.
* **Pipeline Automation:** Stitching data generation, ETL transformations, and presentation services together into a strict chronological workflow execution.
* **Interactive Visualization:** Utilizing Python to spin up dynamic web servers to share actionable corporate metrics without needing front-end web frameworks.

---

## Enterprise Mapping

| Local Tool | Enterprise Equivalent | Project Role |
| :--- | :--- | :--- |
| Python + `Faker` | Operational ERPs (e.g., Pronto Xi) | Generates multi-month transaction files with simulated errors. |
| Local Folders (`data/raw/`) | Cloud Storage / Data Lakes (S3/Blob) | Landing zone for untouched, raw CSV files. |
| Python + `Pandas` | ETL / Transformation Engines (dbt/Spark) | Applies data cleansing rules and structures data fields. |
| CSV Storage (`data/processed/`) | Flat-file staging / Warehousing | Relational-ready storage layer mapping optimized column schemas. |
| Streamlit Server + `Plotly` | Power BI Cloud / Tableau Web Server | Renders interactive, real-time analytics to client browsers. |

---

## Data Cleaning & Transformation Rules
1. **Quarantine Elimination:** Drops missing `invoice_id` records entirely to ensure relational data integrity.
2. **Text Standardization:** Transforms fragmented user strings (e.g., mixing lowercase/uppercase input logs) to forced uppercase layouts (`plan_type`, `payment_status`).
3. **Chronological Realignment:** Maps static timestamps into calendar periods (`Month_Num`, `Month Name`) to permit timeline performance trend logging across the active fiscal year (**2026**).

---

## Project Structure
```text
telecom-edge-dw/
├── data/
│   ├── processed/          # Clean, optimized CSV outputs (e.g., clean_invoices.csv)
│   └── raw/                # Unfiltered operational log streams (e.g., master_raw_traffic.csv)
├── database/               # Dedicated database/warehouse file architecture hooks
├── docs/                   # Supporting project notes and documentation
├── logs/                   # System runtime processing logs
├── src/
│   ├── generate_data.py    # Mock script populating multi-month transactional records
│   ├── pipeline.py         # The Python ETL transformation script
│   └── serve_data.py       # Streamlit server script housing Plotly Express visual charts
├── venv/                   # Isolated Python Virtual Environment directory
└── requirements.txt        # Core package lists (pandas, streamlit, plotly, faker)
```

---

## Deployment & The Daily Execution Loop
The project mimics an enterprise pipeline lifecycle where data must flow sequentially from extraction to loading before it can be served to an interactive dashboard interface.

### Phase 1: Moving Code Across the Environments
Development takes place on a **Windows host computer**, but execution happens on an **Ubuntu Linux Virtual Machine**. To sync changes securely across Port 22, the Secure Copy Protocol (`scp`) is used from the Windows Command Prompt:
```cmd
# Execute inside Windows Command Prompt to push updated code to the VM
cd "C:\Users\Mackay Iria\DataMiningProjects"
scp generate_data.py pipeline.py serve_data.py ubuntu-lab-server@192.168.204.150:~/telecom-edge-dw/src/
```

### Phase 2: Running the Lifecycle Sequence
Switch to your active **Linux terminal session**, ensure your python virtual environment is turned on (`source venv/bin/activate`), and execute the sequential commands:

```bash
# 1. Step 1: Run the data generator to create multi-month records
python3 src/generate_data.py

# 2. Step 2: Run the ETL pipeline to clean strings, remove nulls, and process data
python3 src/pipeline.py

# 3. Step 3: Broadcast the data engine live via port 8501 across the network
streamlit run src/serve_data.py --server.address 0.0.0.0
```

### Phase 3: Viewing the Interactive Output
Once the Streamlit server is active, open any web browser on your local network (such as your host Windows desktop) and visit the live broadcasting link:
```text
http://192.168.204.150:8501
```

The resulting dashboard brings your telecom data to life, displaying:
* **Key Executive Metrics:** Dynamic card charts showing the total sum of invoice revenue, row counts, and attribute metrics.
* **Donut Charts:** Sum of total invoice amounts broken down proportionally by operational regions (*Momase Region (Lae)* vs. *Southern Region (POM)*).
* **Stacked Bar Charts:** Horizontal distribution of revenue categorized across core client plan types.
* **Line Charts:** Interactive revenue performance trend curves tracking growth, peaks, and dips by calendar month name across **2026**.
