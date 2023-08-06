# -*- coding: utf-8 -*-
from outflow.core.command import RootCommand


@RootCommand.subcommand(invokable=False)
def Management():
    pass


@Management.subcommand(with_task_context=True)
def DisplayConfig(self):
    print(self.context.config)
