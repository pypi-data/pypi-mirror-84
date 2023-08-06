#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import pathlib

from outflow.core.logging import logger


class PluginError(Exception):
    """
    Errors related to plugin loading and definitions.
    """


class Plugin:
    """
    Class to manage plugins module of the pipeline.
    """

    @staticmethod
    def _check_and_load_commands(plugin_name, module="commands"):
        """
        Check if the commands module exist and force the import to register the command tree.
        """
        Plugin._check_module(plugin_name, module)

    @staticmethod
    def _check_module(plugin_name, module):
        """
        Check if a module inside the plugin is importable.
        """
        # name for loading
        name = ".".join([plugin_name, module])

        try:
            importlib.import_module(name)
            logger.debug(f"Module {name} successfully imported")
            return True
        except ImportError:
            if plugin_name != "outflow.management":
                logger.warning(
                    "Cannot import module {0} for plugin {1}:".format(
                        module, plugin_name,
                    )
                )
            return False

    @staticmethod
    def load(plugin_name):
        """
        Check the plugin integrity and import the commands.
        """
        Plugin._check_and_load_commands(plugin_name=plugin_name)
        plugin_content = ["models", "commands", "tasks"]
        content = list()
        for module in plugin_content:
            content.append(Plugin._check_module(plugin_name, module))

        if True not in content:
            raise PluginError(
                "An outflow plugin must contain at least one of "
                f"the following modules to be useful : {plugin_content}"
            )

    @staticmethod
    def get_path(plugin_name):
        try:
            return pathlib.Path(
                importlib.import_module(plugin_name).__file__
            ).parent.resolve()
        except ImportError as e:
            logger.print_exception("Cannot find plugin {0}:".format(plugin_name,))
            raise PluginError(e)
