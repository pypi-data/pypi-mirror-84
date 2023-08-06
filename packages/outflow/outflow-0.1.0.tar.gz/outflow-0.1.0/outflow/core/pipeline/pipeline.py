# -*- coding: utf-8 -*-
import argparse
import logging.config
import multiprocessing
import os
import pathlib
import platform
import sys
import time

from outflow import __version__ as outflow_version
from outflow.core.actors import MainActor
from outflow.core.generic.string import as_byte
from outflow.core.logging import logger
from outflow.core.pipeline.context import PipelineContext
from outflow.core.plugin import Plugin


class Pipeline:

    system_arguments = {
        "config": (["--config"], {"help": "The path to the config file."},),
        "settings": (
            ["--settings"],
            {
                "help": 'The Python path to a settings module, e.g. "my_project.my_settings". If this isn\'t provided, the OUTFLOW_SETTINGS_MODULE environment variable will be used.'
            },
        ),
        "version": (
            ["--version"],
            {"help": "Show program's version number and exit.", "action": "store_true"},
        ),
        "python_path": (
            ["--python_path"],
            {
                "help": 'A directory to add to the Python path, e.g. "/home/pipeline_projects/my_project".',
                "action": "append",
                "default": [],
            },
        ),
        "traceback": (["--traceback"], {"help": "Display exception tracebacks."},),
        "no_color": (["--no_color"], {"help": "Don't colorize the command output."},),
        "log_level": (
            ["-ll", "--log-level"],
            {
                "help": "Specifies the amount information that the pipeline should print to the console ",
                "choices": ("DEBUG", "INFO", "WARNING", "ERROR"),
            },
        ),
    }

    base_arguments = {
        "dry_run": (
            ["--dry_run"],
            {"help": "Run the pipeline without the database", "action": "store_true"},
        ),
    }

    def __init__(
        self,
        *,
        root_directory: str = None,
        settings_module: str = "settings",
        argv=None,
        force_dry_run: bool = False,
    ):
        """Init the pipeline instance with the settings, config, descriptor, etc.

        Args:
            root_directory (str, optional): The pipeline directory where the 'manage.py' file is usually located. Defaults to None.
            settings_module (str, optional): The pipeline directory where the 'manage.py' file is usually located. Defaults to 'settings'.
        """
        from outflow.core.pipeline import config as pipeline_config

        self._context = None
        self._root_command = None
        self._job_ids_queue = None
        self._backend = None
        self.force_dry_run = force_dry_run

        if root_directory is not None:
            # ensure both manage.py and settings.py are in the python path
            root_directory_abs_path = pathlib.Path(root_directory).resolve().as_posix()
            os.environ.setdefault("PIPELINE_ROOT_DIRECTORY", root_directory_abs_path)
            sys.path.append(root_directory_abs_path)

        if settings_module is not None:
            os.environ.setdefault("OUTFLOW_SETTINGS_MODULE", settings_module)

        # check pipeline level command line args
        system_args, self.command_argv = self.parse_system_args(argv=argv)

        if system_args.settings is not None:
            os.environ["OUTFLOW_SETTINGS_MODULE"] = system_args.settings

        if system_args.config is not None:
            os.environ["OUTFLOW_CONFIG_PATH"] = (
                pathlib.Path(system_args.config).resolve().as_posix()
            )

        for dir_path in system_args.python_path:
            sys.path.append(pathlib.Path(dir_path).resolve().as_posix())

        # If true, show program's version number and exit.
        self.display_version = system_args.version

        # setup the logger and force the verbose level if needed
        if system_args.log_level is not None:
            pipeline_config["logging"]["loggers"][""]["level"] = system_args.log_level

        logging.config.dictConfig(pipeline_config["logging"])

        logger.debug(f"Config loaded: {pipeline_config}")

        self.load_plugins()

    def load_plugins(self):
        from outflow.core.pipeline import settings

        for plugin_name in settings.PLUGINS:
            Plugin.load(plugin_name)

    @property
    def job_ids_queue(self):
        if self._job_ids_queue is None:
            self._job_ids_queue = multiprocessing.Queue()

        return self._job_ids_queue

    @property
    def context(self):
        if self._context is None:
            self._context = PipelineContext(force_dry_run=self.force_dry_run)

        return self._context

    @property
    def root_command(self):
        if self._root_command is None:
            try:
                from outflow.core.pipeline import settings
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import the pipeline root command from the settings. Are you sure outflow is installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                ) from exc
            # get the instance of the root command singleton
            self._root_command = settings.ROOT_COMMAND_CLASS()

            # loop over the system and base args and add them to the parser to be able to display the full help message
            # if the system arguments have already been added, pass
            base_root_command_args = {**self.system_arguments, **self.base_arguments}
            self.add_args(base_root_command_args, self._root_command.parser)

        return self._root_command

    def add_args(self, args_dict, parser):
        if not getattr(parser, "_args_already_setup", False):

            for argument in args_dict.values():
                parser.add_argument(*argument[0], **argument[1])
            parser._args_already_setup = True

    def parse_system_args(self, argv=None):
        """
        Parse the system args
        """
        parser = argparse.ArgumentParser(
            description="Preprocess system arguments.",
            add_help=False,
            allow_abbrev=False,
        )

        self.add_args(self.system_arguments, parser)

        return parser.parse_known_args(argv)

    @property
    def backend(self):
        if self._backend is None:
            self._backend = "default"
            if (
                "backend" in self.context.config
                and self.context.config["backend"] == "ray"
            ):
                try:
                    import ray  # noqa: F401

                    self._backend = "ray"
                except ImportError:
                    logger.warning(
                        "The 'ray' package is not available, fallback to built-in backend..."
                    )

        return self._backend

    def run(self):
        """Run the pipeline
        """
        if self.display_version:
            print(f"Outflow version '{outflow_version}'")
            return 0

        if self.backend == "ray":
            from outflow.ray.actors import MainActor as RayMainActor

            self.setup_cluster()
            main_actor = RayMainActor(pipeline=self)
        else:
            main_actor = MainActor(context=self.context)

        self.result = self.root_command(self.command_argv, main_actor=main_actor)

        return 0

    @staticmethod
    def get_parent_directory_posix_path(module_path):
        """Return the posix path of the parent directory of the given module

        Args:
            module_path (str): The module path. Usually the one of 'manage.py'

        Returns:
            str: The posix path of the parent directory of the given module
        """
        return pathlib.Path(module_path).parent.resolve().as_posix()

    @staticmethod
    def launch_nodes(node_config: dict, job_ids_q: multiprocessing.Queue):

        from simple_slurm import Slurm

        ray_node = Slurm(
            cpus_per_task=node_config["cpu_per_node"], job_name="ray_node",
        )

        for index in range(node_config["num_nodes"]):
            if index > 0:
                time.sleep(5)

            python_path = sys.executable

            sbatch = (
                "{python_path} -m ray.scripts.scripts start --block --address='{redis_address}' "
                "--num-cpus={num_cpus} "
                "--redis-password='{redis_password}' ".format(
                    python_path=python_path,
                    redis_address=node_config["redis_address"],
                    num_cpus=node_config["cpu_per_node"],
                    # memory=node_config["memory"],
                    redis_password=node_config["redis_password"],
                )
            )

            print(sbatch)

            job_ids_q.put(ray_node.sbatch(sbatch))

    def setup_cluster(self):
        """
        Starts the ray head server, the main worker and sbatch the nodes
        """
        import ray

        # shutdown ray to avoid re-init issues
        ray.shutdown()

        # launch ray head server and main worker
        ray_params = dict()

        cluster_config = self.context.config.get("cluster", {})

        if "mem_per_node" in cluster_config:
            # --- Binary ---
            # 1 MiB = 1024 * 1024
            # 1 MiB = 2^20 bytes = 1 048 576 bytes = 1024 kibibytes
            # 1024 MiB = 1 gibibyte (GiB)

            # --- Decimal ---
            # 1 MB = 1^3 kB = 1 000 000 bytes

            ray_params.update({"_memory": as_byte(cluster_config["mem_per_node"])})
        if "cpu_per_node" in cluster_config:
            ray_params.update({"num_cpus": cluster_config["cpu_per_node"]})

        ray_params.update(
            {"_redis_password": cluster_config.get("redis_password", "outflow")}
        )

        # FIXME: fix ray to support parallel job on windows
        if platform.system() == "Windows":
            ray_params.update({"local_mode": True})
        ray_info = ray.init(**ray_params, resources={"head_node": 1e5})

        cluster_config.update({"redis_address": ray_info["redis_address"]})

        num_nodes = cluster_config.get("num_nodes", 0)

        if num_nodes > 0:
            logger.info(f"Launching {num_nodes} ray nodes")

            self.sbatch_proc = multiprocessing.Process(
                target=self.launch_nodes, args=(cluster_config, self.job_ids_queue),
            )
            self.sbatch_proc.start()

        else:
            logger.info(
                "No cluster config found in configuration file, "
                "running in a local cluster"
            )
