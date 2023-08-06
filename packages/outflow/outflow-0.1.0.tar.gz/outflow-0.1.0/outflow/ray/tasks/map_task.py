# -*- coding: utf-8 -*-
import ray
from outflow.core.tasks.task import Task
from outflow.ray.actors import MapActor


class MapTask(Task):
    def __init__(
        self,
        entrypoint: Task,
        *,
        name=None,
        post_process=lambda x: {"loop_result": x},  # TODO mb change to {output:x}
        inputs=None,
        iterate_on=None,
        outputs=None,
        num_cpus=1
    ):

        super().__init__()

        if iterate_on is None:
            iterate_on = list()
        self._outputs = ["loop_result"]
        if outputs is not None:
            self._outputs += outputs
        if name is not None:
            self.name = name

        self.entrypoint = entrypoint
        self.post_process = post_process

        self._inputs = iterate_on

        self.actor_init_kwargs = {
            "entrypoint": self.entrypoint,
            "post_process": self.post_process,
            "iterate_on": self._inputs,
        }

        self.num_cpus = num_cpus

    def run(self, **loop_inputs):

        loop_workflow = self.entrypoint.workflow
        loop_workflow.entrypoint = self.entrypoint

        actor_results = list()

        for index, generated_inputs in enumerate(self.generator(**loop_inputs)):
            # ensure the workflow entrypoint is the given task
            actor = MapActor.options(num_cpus=self.num_cpus).remote(
                loop_workflow,
                generated_inputs,
                index,
                context=self.context,
                actor_init_kwargs=self.actor_init_kwargs,
            )

            actor_results.append(actor.run.remote())

        result = [
            objid for sublist in ray.get(actor_results) for objid in sublist
        ]  # TODO remove this
        return self.post_process(result)

    def generator(self, **loop_inputs):
        """
        default generator function
        :param loop_inputs:
        :return:
        """

        inputs = loop_inputs.copy()

        if len(self._inputs) == 1:
            for key, val in self.entrypoint.inputs.items():
                target_class, args, kwargs = val
                if kwargs.get("mapped", False):
                    del inputs[self._inputs[0]]
                    task_input_name = key
                    for input_arg in loop_inputs[self._inputs[0]]:  # TODO change
                        yield {task_input_name: input_arg, **inputs}
        else:
            pass  # TODO
