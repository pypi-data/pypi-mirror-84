# -*- coding: utf-8 -*-
import subprocess

import ray
from outflow.core.actors.main_actor import MainActor as CoreMainActor
from outflow.core.logging import logger


@ray.remote
class _RayMainActor(CoreMainActor):
    pass


class MainActor:
    def __init__(
        self, pipeline, num_cpus=1, resources={"head_node": 1}, *args, **kwargs
    ):
        self.pipeline = pipeline
        self.ray_actor = _RayMainActor.options(
            resources=resources, num_cpus=num_cpus
        ).remote(context=self.pipeline.context)

    def update_pipeline_context_args(self, pipeline_args):
        self.ray_actor.update_pipeline_context_args.remote(pipeline_args)

    def run(self, *, task_list=[]):
        main_actor_result = self.ray_actor.run.remote(task_list=task_list)

        try:
            result = ray.get(main_actor_result)
            return result
        except TypeError as te:
            if "missing 1 required positional argument: 'task_context'" in te.args[0]:
                print('Task expected a context but "with_context" is False')
                raise
        finally:
            if hasattr(self, "sbatch_proc"):
                self.pipeline.sbatch_proc.terminate()
            while not self.pipeline.job_ids_queue.empty():
                slurm_id = self.pipeline.job_ids_queue.get()
                logger.info("cancelling slurm id {id}".format(id=slurm_id))
                subprocess.run(["scancel", str(slurm_id)])

        return 0
