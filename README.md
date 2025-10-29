# Project_pipline_Analysis
# 🚀 AirflowProject - Sales Revenue Analysis Pipeline

A complete data pipeline using Apache Airflow to analyze daily sales revenue from PostgreSQL.

![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![Airflow](https://img.shields.io/badge/Apache-Airflow-017CEE?logo=apacheairflow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-336791?logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.8-3776AB?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## 📊 Project Overview

This project demonstrates an end-to-end data pipeline that:
- 📈 Extracts sales data from PostgreSQL database
- 💰 Calculates daily revenue metrics
- 📊 Generates automated reports and visualizations
- ⚡ Automates the entire workflow using Apache Airflow

- 
## 🏗️ Pipeline Architecture
flowchart LR
    A[PostgreSQL Database] -->|Extract| B[Airflow DAG]
    B -->|Transform| C[Data Processing - Pandas]
    C -->|Visualize| D[Matplotlib Charts]
    C -->|Export| E[CSV / Reports]

## 🛠️ Tech Stack

- **Apache Airflow 2.8.1** - Workflow orchestration
- **PostgreSQL 13** - Relational database
- **Python 3.8** - Data processing
- **Docker & Docker Compose** - Containerization
- **Pandas** - Data manipulation
- **Matplotlib** - Data visualization

## 🚀 Quick Start

### Prerequisites
- 🐳 Docker
- 🐳 Docker Compose

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ahmedsalah554/AirflowProject.git
   cd AirflowProject
2-Start the services
 docker-compose up -d

 3-Access Airflow UI

 🌐 URL: http://localhost:8080

 👤 Username: Your_Name

 🔑 Password: Your_Pass

4-Configure PostgreSQL Connection

 Navigate to Admin → Connections 

 Add new connection: postgres_default

 Type: Postgres

 Host: postgres

 Database: sales_project_db

 Username: Your_Name

 Password: Your_Pass

 Port: Your_port_Num

5-Trigger the Pipeline

 Enable sales_revenue_pipeline DAG

 Click trigger button to start the analysis

📁 Project Structure


AirflowProject/
├── dags/                    # Airflow DAGs and workflows
├── logs/                    # Airflow execution logs
├── plugins/                 # Custom Airflow plugins
├── data/                    # Generated reports and output files
├── docker-compose.yml       # Docker service orchestration
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── LICENSE                  # MIT License
└── scripts/                 # Utility and helper scripts



🔧 Pipeline Tasks
sales_revenue_pipeline DAG
Task	Description	Output
create_sales_table	Creates and populates sales table	PostgreSQL table
calculate_daily_revenue	Computes daily revenue metrics	CSV file
visualize_revenue	Generates revenue charts	PNG images
generate_report	Creates summary reports	Text report
📈 Sample Data Schema
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    product_name VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);
🎯 Features
✅ Automated Data Pipeline - End-to-end automation

✅ Database Integration - PostgreSQL connectivity

✅ Data Visualization - Matplotlib charts

✅ Report Generation - Comprehensive analytics

✅ Containerized - Docker deployment

✅ Scalable - Easy to extend and modify
🐛 Troubleshooting
Common Issues
Connection Issues:
# Check service status
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres
DAG Import Errors:

Verify Python packages in requirements.txt

Check DAG file syntax

Port Conflicts:
# Modify in docker-compose.yml
ports:
  - "8081:8080"  # Use alternative port
  🧪 Testing
  # List all DAGs
docker exec airflow-webserver-1 airflow dags list

# Test specific task
docker exec airflow-webserver-1 airflow tasks test sales_revenue_pipeline create_sales_table 2024-01-01

# Check task execution
docker exec airflow-webserver-1 airflow tasks list sales_revenue_pipeline
🔄 Monitoring
Airflow UI: http://localhost:8080

PostgreSQL: localhost:5432

Logs: docker-compose logs [service_name]

🤝 Contributing
We welcome contributions! Please follow these steps:

🍴 Fork the project

🌿 Create your feature branch (git checkout -b feature/AmazingFeature)

💾 Commit your changes (git commit -m 'Add some AmazingFeature')

📤 Push to the branch (git push origin feature/AmazingFeature)

🔔 Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author
Ahmed Salah

GitHub: @Ahmedsalah554

Project: AirflowProject

🙏 Acknowledgments
Apache Airflow community

PostgreSQL development team

Docker ecosystem

Python data science community

⭐ If you find this project helpful, please give it a star on GitHub!
