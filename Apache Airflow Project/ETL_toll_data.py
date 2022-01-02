# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Daniel',
    'start_date': days_ago(0),
    'email': ['daniel@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -zxvf tolldata.tgz',
    dag=dag,
)


# define the second task
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1,2,3,4 vehicle-data.csv > csv_data.csv',
    dag=dag,
)

# define the third task
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cat tollplaza-data.tsv | tr "\\t" "," | cut -d"," -f5,6,7 > tsv_data.csv',
    dag=dag,
)

# define the fourth task
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cat payment-data.txt | tr " " "," | cut -b 58-66 > fixed_width_data.csv',
    dag=dag,
)

# define the fifth task
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste -d "," csv_data.csv tsv_data.csv fixed_width_data.csv | tr -d "\r" | tr -s "," > extracted_data.csv',
    dag=dag,
)

# task pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data