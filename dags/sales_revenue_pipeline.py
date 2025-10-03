from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os, glob

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def create_sales_table():
    hook = PostgresHook(postgres_conn_id='postgres_default')
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        order_date DATE NOT NULL,
        product_name VARCHAR(100),
        quantity INTEGER,
        unit_price DECIMAL(10,2),
        total_amount DECIMAL(10,2)
    );
    """
    hook.run(create_table_sql)
    hook.run("DELETE FROM sales;")
    insert_data_sql = """
    INSERT INTO sales (order_date, product_name, quantity, unit_price, total_amount)
    VALUES 
        ('2024-01-01', 'Laptop', 2, 1500.00, 3000.00),
        ('2024-01-01', 'Mouse', 5, 25.50, 127.50),
        ('2024-01-02', 'Keyboard', 3, 75.00, 225.00),
        ('2024-01-02', 'Monitor', 1, 800.00, 800.00),
        ('2024-01-03', 'Laptop', 1, 1500.00, 1500.00),
        ('2024-01-03', 'Headphones', 4, 50.00, 200.00),
        ('2024-01-04', 'Tablet', 2, 600.00, 1200.00),
        ('2024-01-04', 'Mouse', 3, 25.50, 76.50);
    """
    hook.run(insert_data_sql)
    print("✅ Sales table created and data inserted")

def calculate_daily_revenue():
    hook = PostgresHook(postgres_conn_id='postgres_default')
    sql_query = """
    SELECT order_date, SUM(total_amount) as daily_revenue
    FROM sales
    GROUP BY order_date
    ORDER BY order_date;
    """
    connection = hook.get_conn()
    df = pd.read_sql(sql_query, connection)
    connection.close()
    os.makedirs('/opt/airflow/data', exist_ok=True)
    df.to_csv('/opt/airflow/data/daily_revenue.csv', index=False)
    print("✅ Daily revenue data saved to CSV")
    print(df)

def visualize_revenue():
    import matplotlib
    matplotlib.use('Agg')
    df = pd.read_csv('/opt/airflow/data/daily_revenue.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['order_date'], df['daily_revenue'], marker='o', linewidth=2, markersize=8, color='#2E86AB')
    plt.title('Daily Revenue Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Revenue ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs('/opt/airflow/data/revenue_plots', exist_ok=True)
    plot_path = f'/opt/airflow/data/revenue_plots/daily_revenue_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Revenue plot saved: {plot_path}")

def generate_report():
    df = pd.read_csv('/opt/airflow/data/daily_revenue.csv')
    total_revenue = df['daily_revenue'].sum()
    avg_daily_revenue = df['daily_revenue'].mean()
    max_revenue_day = df.loc[df['daily_revenue'].idxmax()]
    min_revenue_day = df.loc[df['daily_revenue'].idxmin()]
    report = f"""
    📊 DAILY REVENUE REPORT 📊
    ================================
    Total Period: {len(df)} days
    Total Revenue: ${total_revenue:,.2f}
    Average Daily Revenue: ${avg_daily_revenue:,.2f}
    Best Performing Day: {max_revenue_day['order_date']} - ${max_revenue_day['daily_revenue']:,.2f}
    Lowest Revenue Day: {min_revenue_day['order_date']} - ${min_revenue_day['daily_revenue']:,.2f}
    ================================
    """
    with open('/opt/airflow/data/revenue_report.txt', 'w') as f:
        f.write(report)
    print("✅ Revenue report generated")

def get_latest_plot():
    plot_files = glob.glob('/opt/airflow/data/revenue_plots/*.png')
    if not plot_files:
        return None
    return max(plot_files, key=os.path.getctime)

with DAG(
    'sales_revenue_pipeline',
    default_args=default_args,
    description='Pipeline to analyze sales revenue',
    schedule_interval='@daily',
    catchup=False,
    tags=['sales', 'revenue']
) as dag:

    create_table_task = PythonOperator(
        task_id='create_sales_table',
        python_callable=create_sales_table
    )

    calculate_revenue_task = PythonOperator(
        task_id='calculate_daily_revenue',
        python_callable=calculate_daily_revenue
    )

    visualize_revenue_task = PythonOperator(
        task_id='visualize_revenue',
        python_callable=visualize_revenue
    )

    generate_report_task = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report
    )

    send_email_task = EmailOperator(
        task_id='send_email_report',
        to='salahabdelniem@gmail.com',  # ← غيّرها لإيميلك
        subject='📊 Daily Sales Revenue Report',
        html_content="<h3>Attached are today's sales revenue results.</h3>",
        files=[
            '/opt/airflow/data/daily_revenue.csv',
            '/opt/airflow/data/revenue_report.txt',
            get_latest_plot()
        ]
    )

    create_table_task >> calculate_revenue_task >> [visualize_revenue_task, generate_report_task] >> send_email_task
