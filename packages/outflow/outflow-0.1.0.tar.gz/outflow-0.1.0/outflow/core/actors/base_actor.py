# -*- coding: utf-8 -*-
from outflow.core.logging import logger


class BaseActor:
    def __init__(self, context=None, actor_init_kwargs=None):
        logger.debug(f"Initialize actor '{self}'")
        self.pipeline_context = context
        if actor_init_kwargs is None:
            actor_init_kwargs = dict()
        self.__dict__.update(**actor_init_kwargs)

    def update_pipeline_context_args(self, pipeline_args):
        logger.debug(
            f"Update pipeline context '{self.pipeline_context}' with args '{pipeline_args}'"
        )
        self.pipeline_context.args = pipeline_args
