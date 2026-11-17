# import sys
# from airflow import DAG
# from airflow.providers.docker.operators.docker import DockerOperator
# from datetime import datetime, timedelta
# from docker.types import Mount


# default_args = {
#     'description':'A DAG to orchestrate data',
#     'start_date':datetime(2024, 4, 30),
    
# }

# dag = DAG(
#     dag_id='weather-dbt-orchestrator',
#     default_args=default_args,
#     schedule=timedelta(minutes=5),
#     catchup=False,
# )

# with dag:
#     task1 = PythonOperator(
#         task_id='ingest_data_task',
#         python_callable=safe_main_callable  
#     )
    
#     task2 = DockerOperator(
#         task_id='transform_data_task',
#         image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
#         command='run',
#         working_dir='/usr/app',
#         Mounts=[
#             Mount(source='/home/lenovo/repos/weather-data-project/dbt/my_project',
#                   target='/usr/app',
#                   type='bind'),
#             Mount(source='/home/lenovo/repos/weather-data-project/dbt',
#                   target='/root/.dbt/',
#                   type='bind'),
#             ],
#         network_mode='my_network',
#         docker_url='unix://var/run/docker.sock',
#         auto_remove='success'
#     )

# import sys
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.providers.docker.operators.docker import DockerOperator
# from datetime import datetime, timedelta
# from docker.types import Mount

# def safe_main_callable():
#     import sys
#     if '/opt/airflow/api-request' not in sys.path:
#         sys.path.append('/opt/airflow/api-request')
#     from insert_records import main
#     return main()

# default_args = {
#     'description': 'A DAG to orchestrate data',
#     'start_date': datetime(2024, 4, 30),
# }

# dag = DAG(
#     dag_id='weather-dbt-orchestrator',
#     default_args=default_args,
#     schedule=timedelta(minutes=5),
#     catchup=False,
# )

# with dag:
#     task1 = PythonOperator(
#         task_id='ingest_data_task',
#         python_callable=safe_main_callable
#     )

    # task2 = DockerOperator(
    #     task_id='transform_data_task',
    #     image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
    #     command='run',
    #     working_dir='/usr/app',
    #     mounts=[
    #         Mount(
    #             source='/home/lenovo/repos/weather-data-project/dbt/my_project',
    #             target='/usr/app',
    #             type='bind'
    #         ),
    #         Mount(
    #             source='/home/lenovo/repos/weather-data-project/dbt',
    #             target='/root/.dbt/',
    #             type='bind'
    #         ),
    #     ],
    #     network_mode='weather-data-project_my_network',
    #     docker_url='unix://var/run/docker.sock',
    #     auto_remove='success'
    # )

    # task1 >> task2
