import copy

from prunner import loaders
from prunner.tasks import STANDARD_TASKS
from prunner.util import shellexpand


class Executioner:
    def __init__(
        self, config_dir, variables, dryrun=False, verbose=False, tasks=STANDARD_TASKS
    ):
        self.variables = {
            "PRUNNER_CONFIG_DIR": config_dir,
            "DRYRUN": dryrun,
            "VERBOSE": verbose,
            **variables,
        }
        yaml_file = f"{config_dir}/pipelines.yaml"
        self.pipeline_loader = loaders.YamlLoader(yaml_file)

        self.tasks = {}
        self.add_tasks(tasks)

    def add_tasks(self, tasks):
        for task in tasks:
            task_instance = task.from_settings(self.variables)
            self.tasks[task.task_name()] = task_instance

    def execute_pipeline(self, pipeline_name):
        self.variables["PIPELINE_NAME"] = pipeline_name
        pipeline = self.pipeline_loader.get_section(pipeline_name)

        for i, raw_task_dict in enumerate(pipeline):
            raw_task_dict = copy.deepcopy(raw_task_dict)
            task_name, task_params = raw_task_dict.popitem()

            task = self.get_task(task_name)
            task_params = task.modify_params(task_params, self.variables)
            self.print_new_task(i, task_name, task_params)

            updates = self.run_task(task, task_params)
            self.handle_verbose_flag(updates)
            self.variables = {
                **self.variables,
                **updates,
            }

    def get_task(self, task_name):
        if task_name not in self.tasks:
            raise ValueError("That task is not available: ", task_name)
        task = self.tasks[task_name]
        return task

    def handle_verbose_flag(self, updates):
        if self.variables["VERBOSE"]:
            new_variables = {
                k: v for k, v in updates.items() if k not in self.variables
            }
            mutations = {k: v for k, v in updates.items() if k in self.variables}
            print("Mutations = ", mutations)
            print("New Values = ", new_variables)

    def run_task(self, task, params):
        updates = task.execute(params, self.variables)
        if updates is None or type(updates) != dict:
            updates = {}
        return updates

    def print_new_task(self, i, task_name, task_value):
        print("-" * 80)
        print(f"Task {i}: {task_name} = {task_value}")
