"""
BEST PRACTICE: Document your DAG by putting in a docstring to explain at a high level
what problem space the DAG is looking at. Including links to design documents, upstream dependencies etc
are highly recommended. Note that by doing this, it will flow through to the AirFlow UI so you can actually
see this when using the Scheduler. It is important to include dag.doc_md = __doc__ in your code for this to work.
"""
# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


from builtins import range
from datetime import timedelta

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

'''
    CHANGE the name of your DAG when you change the start date, using the Version in the dag_id 
    Changing the start_date of a DAG creates a new entry in Airflow's database, which could confuse the scheduler
    because there will be two DAGs with the same name but different schedules.
    Changing the name of a DAG also creates a new entry in the database, which powers the dashboard, 
    so follow a consistent naming convention since changing a DAG's name doesn't delete the entry in the database
    for the old name.
'''
dag = DAG(
    dag_id='Lendkey_DagTemplate-Simple-V1',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=['This is a simple DAG template - start with this.']
)

dag.doc_md = __doc__  #This will force the docstring to flow to the UI.

run_this_last = DummyOperator(
    task_id='run_this_last',
    dag=dag,
)

# [START howto_operator_bash]
run_this = BashOperator(
    task_id='run_after_loop',
    bash_command='echo 1',
    dag=dag,
)
# [END howto_operator_bash]

run_this >> run_this_last

for i in range(3):
    task = BashOperator(
        task_id='runme_' + str(i),
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        dag=dag,
    )
    task >> run_this

# [START howto_operator_bash_template]
also_run_this = BashOperator(
    task_id='also_run_this',
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag,
)
# [END howto_operator_bash_template]
also_run_this >> run_this_last

if __name__ == "__main__":
    dag.cli()