#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from alembic import op

logger = logging.getLogger("alembic")

__all__ = ["create_schema", "create_table", "execute"]


"""
    These functions are wrappers around alembic execute() and table/schema
    creation and deletion in order to control authorisations on tables/schemas
    and set up a logger
"""


def get_login_info():
    # retrieve login info from the configuration
    from outflow.core.pipeline import config, settings

    login_info = config["pipeline"]["databases"][settings.MAIN_DATABASE]["login_info"]
    admin = login_info["admin"].split(":")[0]
    user = login_info["user"].split(":")[0]
    return admin, user


def execute(cmd):
    """Calls logger before executing a SQL command"""
    logger.info(cmd)
    op.execute(cmd)


def create_table(table_name, *args, **kwargs):
    """ Create a table and grant the corresponding access to users"""
    op.create_table(table_name, *args, **kwargs)

    admin, user = get_login_info()

    try:
        table_name = f'{kwargs["schema"]}.{table_name}'
    except KeyError:
        pass

    grant_user = f"GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE {table_name} TO {user}"
    grant_admin = f"GRANT ALL ON TABLE {table_name} TO {admin}"

    execute(grant_user)
    execute(grant_admin)


def create_schema(schema_name):
    """ Create a schema and grant the corresponding access to users"""

    admin, user = get_login_info()

    execute("CREATE SCHEMA IF NOT EXISTS {}".format(schema_name))

    grant_user = "GRANT USAGE ON SCHEMA {0} TO {1}".format(schema_name, user)

    grant_admin = "GRANT ALL ON SCHEMA {0} TO {1}".format(schema_name, admin)

    execute(grant_user)
    execute(grant_admin)


def drop_schema(schema_name, cascade=False):
    """ Drop a schema """

    execute(f'DROP SCHEMA {schema_name} {"CASCADE" if cascade else ""}')


def drop_table(table_name, schema=None):
    """ Drop a table """

    if schema:
        table_name = schema + "." + table_name

    execute(f"DROP TABLE IF EXISTS {table_name}")
