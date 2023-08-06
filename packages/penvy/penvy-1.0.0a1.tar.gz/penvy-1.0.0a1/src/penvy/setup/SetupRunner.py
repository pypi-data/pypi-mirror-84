from logging import Logger, DEBUG
from typing import List
from penvy.setup.SetupStepInterface import SetupStepInterface


class SetupRunner:
    def __init__(
        self,
        steps: List[SetupStepInterface],
        logger: Logger,
    ):
        self._steps = steps
        self._logger = logger

    def run(self):
        is_verbose = self._logger.level == DEBUG

        for step in self._get_steps2skip():
            description = self._get_description(step, is_verbose)
            self._logger.debug(f"Skipping: {description}")

        for step in self._get_steps2run():
            description = self._get_description(step, is_verbose)
            self._logger.debug(f"Running: {description}")
            step.run()

    def show(self):
        self._logger.info("Setup steps to run:")

        is_verbose = self._logger.level == DEBUG
        index = 1

        for step in self._get_steps2run():
            description = self._get_description(step, is_verbose)
            self._logger.info(f"{index}. {description}")
            index += 1

    def _get_steps2run(self):
        return list(filter(lambda step: step.should_be_run(), self._steps))

    def _get_steps2skip(self):
        return list(filter(lambda step: not step.should_be_run(), self._steps))

    def _get_description(self, step: SetupStepInterface, is_verbose):
        return f"{step.get_description()}" + (f" ({step.__module__})" if is_verbose else "")
