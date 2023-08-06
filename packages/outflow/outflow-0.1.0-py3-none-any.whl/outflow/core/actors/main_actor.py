# -*- coding: utf-8 -*-
from outflow.core.actors.base_actor import BaseActor
from outflow.core.logging import logger
from outflow.core.tasks.task_manager import TaskManager


class MainActor(BaseActor):
    def __init__(self, context, *args, **kwargs):
        super().__init__(*args, context=context, **kwargs)

    def run(self, *, task_list):
        logger.debug(
            f"Run pipeline in actor '{self}' with pipeline context '{self.pipeline_context}'"
        )
        task_manager = TaskManager()

        for task in task_list:
            task.workflow.set_context(self.pipeline_context)
            task_manager.compute(task.workflow)

        return [task_manager.results.resolve(task.id) for task in task_list]
