\# Sales Analysis



\## Table of Contents



\- \[Objectives](#objectives)

\- \[Repository Structure](#repository-structure)

\- \[How to Use](#how-to-use)

\- \[Contributing](#contributing)

\- \[License](#license)

\## Project Overview



`sales-analysis` is a Python project for \*\*analyzing sales data\*\* from an Excel file.  

It automates the creation of \*\*statistical tables\*\* and \*\*visual reports\*\* (PDF, ODF, charts) to answer key business questions about sales performance, including revenue, quantity, and price dispersion.



The goal is to provide a \*\*modular, reproducible, and maintainable tool\*\* for data-driven insights on sales.



\[Back to Top](#sales-analysis)

\## Objectives



The goal of this project is to provide a \*\*comprehensive and automated framework\*\* for analyzing sales data.  

It is designed to help understand sales performance, identify trends, measure productivity of salespeople, and support data-driven decision-making.  



Specifically, the project enables:



\- Aggregation of sales data by various dimensions (time, salesperson, product, etc.)

\- Calculation of key performance metrics such as revenue, quantity, and average transaction values

\- Identification of patterns, outliers, and variability in sales and pricing

\- Generation of professional reports and visualizations (PDF, ODF, charts) for stakeholders



Some example analyses the project can perform include:



&nbsp;   1. Total revenue per year per salesperson (PDF table)  

&nbsp;   2. Average revenue per quarter per salesperson (ODF table)  

&nbsp;   3. Average quantity sold per transaction per salesperson  

&nbsp;   4. Salesperson with the highest unit price dispersion in 2023 (PDF histogram)  

&nbsp;   5. Ranking of salespeople in 2025 by average revenue per transaction (PDF table)  

&nbsp;   6. Min, max, and average revenue per salesperson over the full period (PDF table)  

&nbsp;   7. Salesperson with the highest median revenue in 2023 (PDF table)  

&nbsp;   8. Total number of transactions per year per salesperson (PDF histogram)  



\[Back to Top](#sales-analysis)

\## Project Structure

```bash

sales-analysis/

│

├── data/                        # Input Excel file (ventes.xlsx)

├── output/                      # Generated results

│   ├── tables/                  # Exported PDF / ODF tables

│   ├── charts/                  # PDF/PNG charts

│   └── reports/                 # Full reports

│

├── src/                         # Source code

│   ├── data\_loader.py           # Load and preprocess Excel data

│   ├── analysis.py              # Analytical functions

│   ├── report\_generator.py      # Export tables and charts

│   ├── main.py                  # Main script to run analysis

│   └── utils.py                 # Utility functions

│

├── requirements.txt             # Python dependencies

├── README.md                    # Project documentation

└── .gitignore                   # Ignored files for Git

```



\[Back to Top](#sales-analysis)

\## Installation



1\. Clone the repository

```bash

git clone https://github.com/EssYassine/sales-analysis.git

cd sales-analysis

```

2\. Create a virtual environment

```bash

python -m venv .venv

\# Windows

.venv\\Scripts\\activate

\# Linux / macOS

source .venv/bin/activate

```

3\. Install dependencies

```bash

pip install -r requirements.txt

```



4\. Place your Excel file in the data/ folder (Data\_Load.xlsx)

\## Usage



Run the main script:

```bash

python -m src.main

```

\- Tables (PDF/ODF) and charts will be automatically generated in the output/ folder.

\- Check output/tables/ for tables, output/charts/ for graphs.

