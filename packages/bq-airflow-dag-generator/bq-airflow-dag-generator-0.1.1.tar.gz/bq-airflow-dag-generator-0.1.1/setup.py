# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bq_airflow_dag_generator']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=1.10.12,<2.0.0',
 'google-cloud-bigquery>=2.3.1,<3.0.0',
 'networkx>=2.5,<3.0',
 'pydot>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'bq-airflow-dag-generator',
    'version': '0.1.1',
    'description': 'Generate Airflow DAG from DOT language to execute BigQuery efficiently mainly for AlphaSQL',
    'long_description': None,
    'author': 'Matts966',
    'author_email': 'Matts966@users.noreply.github.com ',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
