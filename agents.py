import numpy as np

from supplements import Result, Task


class BaseAgent:
    id = 0
    __surnames = ['Smith', 'Johnson',
                  'Williams', 'Brown',
                  'Jones', 'Garcia',
                  'Miller', 'Davis',
                  'Anderson', 'Taylor']
    __first_names = ['Liam', 'Noah',
                     'Olivia', 'Emma',
                     'Oliver', 'Amelia',
                     'Henry', 'Mia',
                     'Lucas', 'Evelyn']

    def __init__(self, role):
        self.id = BaseAgent.id
        BaseAgent.id += 1
        self.role = role
        self.name = " ".join([np.random.choice(self.__first_names), np.random.choice(self.__surnames)])


class Intern(BaseAgent):

    def update_efficiency(self):
        self.efficiency = self.successes / self.attempts

    def generate_outcome(self, hard_task):
        if hard_task:
            self.outcomes.append(Result(success_rate=self.success_rate * .8,
                                        mean_time=self.mean_time * 2, std=self.deviation))
        else:
            self.outcomes.append(Result(success_rate=self.success_rate,
                                        mean_time=self.mean_time, std=self.deviation))

    def __init__(self):
        super().__init__(role='Intern')
        self.success_rate = np.random.choice([x / 10 for x in range(6, 10, 1)], p=[0.2, 0.3, 0.3, 0.2])
        self.fall_rate = 1 - self.success_rate
        self.mean_time = np.random.choice(range(8, 14, 2))
        self.deviation = np.random.choice([x / 10 for x in range(5, 20, 5)])
        self.outcomes = []
        self.attempts = 0
        self.successes = 0
        self.efficiency = 0.5


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
        return len(self.__pipeline)

    @property
    def pipeline(self):
        return self.__pipeline

    @pipeline.setter
    def pipeline(self, value):
        self.__pipeline.append(value)

    # def assign(self, value):
    #     self.pipeline.append(value)
    #
    # def release(self, value):
    #     idx = self.pipeline.index(value)
    #     self.completed.append(self.pipeline.pop(idx))

    def handler(self):
        pass

    def __init__(self):
        super().__init__(role='Physician')
        self.qualification = np.random.choice(['Doctor of Medical Sciences',
                                               'Candidate of Medical Sciences',
                                               'Specialist'], p=[0.2, 0.3, 0.5])
        self.__completed = []
        self.__pipeline = []
        self.__workload = 0
