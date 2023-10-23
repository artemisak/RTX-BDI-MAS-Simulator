import asyncio
import configparser
import time
from datetime import timedelta

import numpy as np

from supplements import Result, Task

config = configparser.ConfigParser()
config.read("config.ini")


class BaseAgent:
    id = 0
    _surnames = config["NAMES"]["LAST_NAMES"].split(sep=', ')
    _first_names = config["NAMES"]["FIRST_NAMES"].split(sep=', ')

    def __init__(self, role):
        self.id = BaseAgent.id
        BaseAgent.id += 1
        self.role = role
        self.name = " ".join([np.random.choice(self._first_names), np.random.choice(self._surnames)])


class Intern(BaseAgent):

    @property
    def efficiency(self):
        return self.successes / self.attempts

    @property
    def successes(self):
        return len([x for x in self.outcomes if x.result == 1])

    @property
    def attempts(self):
        return len(self.outcomes)

    def generate_outcome(self, task):
        if task.intricate:
            result = Result(success_rate=self.success_rate * .8,
                            mean_time=self.mean_time * 2, std=self.deviation)
            self.outcomes.append(result)
            return result
        else:
            result = Result(success_rate=self.success_rate,
                            mean_time=self.mean_time, std=self.deviation)
            self.outcomes.append(result)
            return result

    def __init__(self):
        super().__init__(role='Intern')
        self.success_rate = np.random.choice([x / 10 for x in range(6, 10, 1)], p=[0.2, 0.3, 0.3, 0.2])
        self.mean_time = np.random.choice(range(8, 14, 2))
        self.deviation = np.random.choice([x / 10 for x in range(5, 20, 5)])
        self.outcomes = []
        self._attempts = 0
        self._successes = 0
        self._efficiency = 0.5


class Patient(BaseAgent):

    @staticmethod
    def createTask():
        return Task()

    def choosePhysician(self, available_physicians):
        executor = np.random.choice(available_physicians)
        executor.pipeline = self
        return executor

    def __init__(self, income_time, available_physicians):
        super().__init__(role='Patient')
        self.income_time = income_time
        self.resume_time = None
        self.task = self.createTask()
        self.physician = self.choosePhysician(available_physicians)


class Physician(BaseAgent):

    @property
    def workload(self):
        return len(self._pipeline)

    @property
    def pipeline(self):
        return self._pipeline

    @pipeline.setter
    def pipeline(self, request):
        self.assign(request)
        asyncio.create_task(self.solve(request, self.assistants))

    @staticmethod
    def choose_intern(pool):
        return np.random.choice(pool)

    async def solve(self, objective, assistants):
        intern = self.choose_intern(assistants)
        result = 0
        latency = timedelta(minutes=0)
        while result == 0:
            outcome = intern.generate_outcome(objective.task)
            result = outcome.result
            if result == 0:
                latency = outcome.time + timedelta(minutes=np.random.choice(range(1, 4)))
            else:
                latency = outcome.time + timedelta(minutes=np.random.choice(range(7, 10)))
        objective.resume_time = objective.income_time + latency
        time.sleep(0.87)
        self.release(objective)

    def assign(self, objective):
        self._pipeline.append(objective)

    def release(self, objective):
        idx = self.pipeline.index(objective)
        self.completed.append(self.pipeline.pop(idx))

    def __init__(self, assistants):
        super().__init__(role='Physician')
        self.qualification = np.random.choice(['Doctor of Medical Sciences',
                                               'Candidate of Medical Sciences',
                                               'Specialist'], p=[0.2, 0.3, 0.5])
        self.assistants = assistants
        self.completed = []
        self._pipeline = []
        self._workload = 0
