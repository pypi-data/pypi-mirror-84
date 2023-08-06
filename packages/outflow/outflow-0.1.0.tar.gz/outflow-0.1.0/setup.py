# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['outflow',
 'outflow.core',
 'outflow.core.actors',
 'outflow.core.db',
 'outflow.core.db.alembic',
 'outflow.core.generic',
 'outflow.core.library',
 'outflow.core.logging',
 'outflow.core.pipeline',
 'outflow.core.pipeline.settings_management',
 'outflow.core.tasks',
 'outflow.core.test',
 'outflow.management',
 'outflow.management.commands',
 'outflow.management.models',
 'outflow.management.models.versions',
 'outflow.management.templates.pipeline_template',
 'outflow.ray',
 'outflow.ray.actors',
 'outflow.ray.tasks']

package_data = \
{'': ['*'],
 'outflow.management': ['templates/plugin_template/*',
                        'templates/plugin_template/plugin_namespace/*',
                        'templates/plugin_template/plugin_namespace/plugin_name/*',
                        'templates/plugin_template/plugin_namespace/plugin_name/models/*',
                        'templates/plugin_template/plugin_namespace/plugin_name/models/versions/*']}

install_requires = \
['aiohttp==3.6.2',
 'alembic==1.4.3',
 'cloudpickle==1.5.0',
 'declic>=1.0.2,<2.0.0',
 'jinja2==2.11.2',
 'networkx>=2.4,<3.0',
 'psycopg2-binary==2.8.6',
 'ray>=1.0.0,<2.0.0',
 'simple-slurm==0.1.5',
 'sqlalchemy==1.3.20',
 'toml==0.10.1',
 'typeguard>=2.7.1,<3.0.0',
 'typing-extensions==3.7.4.2']

setup_kwargs = {
    'name': 'outflow',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gregoire Duvauchelle',
    'author_email': 'gregoire.duvauchelle@lam.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
