import datetime
import time

import numpy as np


class Simulator:
    start_time = datetime.datetime.now()
    patients = []
    physicians = []

    @staticmethod
    def generate_patients(intensity=5, time_span=30, size=1):
        last = Simulator.start_time
        for latency in np.round(np.random.exponential(scale=time_span / intensity, size=size)):
            last += datetime.timedelta(minutes=latency)
            Simulator.patients.append(Patient(income_time=last))

    @staticmethod
    def generate_physicians():
        Simulator.physicians = [Physician() for _ in range(1, 5)]

    def run_simulation(self):
        self.generate_physicians()
        i = 0
        while i < 10:
            self.generate_patients()

            print('\n\n\n')
            for physician in self.physicians:
                print(physician.id, physician.role, physician.name,
                      physician.qualification, physician.workload,
                      [i.id for i in physician.pipeline])

            for patient in self.patients:
                print(patient.id, patient.role, patient.name, patient.physician.id, patient.task.urgency,
                      patient.task.intricate)

            i += 1
            time.sleep(1)

    def __init__(self, start_datetime=None):
        if start_datetime:
            Simulator.start_time = datetime.datetime.strptime(start_datetime,
                                                              '%d.%m.%Y %H:%M')


class Agent:
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
        self.id = Agent.id
        Agent.id += 1
        self.role = role
        self.name = " ".join([np.random.choice(self.__first_names), np.random.choice(self.__surnames)])


class Intern(Agent):

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


class Physician(Agent):

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


class Patient(Agent):

    @staticmethod
    def createTask():
        return Task()

    def choosePhysician(self):
        executor = np.random.choice(Simulator.physicians)
        executor.pipeline = self
        return executor

    def __init__(self, income_time):
        super().__init__(role='Patient')
        self.income_time = income_time
        self.resume_time = None
        self.task = self.createTask()
        self.physician = self.choosePhysician()


class Result:
    def __init__(self, success_rate, mean_time, std):
        self.result = np.random.choice([0, 1], p=[1 - success_rate, success_rate])
        self.time = np.random.normal(mean_time, std)


class Task:
    def __init__(self):
        self.urgency = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
        self.intricate = np.random.choice([True, False], p=[0.3, 0.7])


if __name__ == '__main__':
    instance = Simulator()
    instance.run_simulation()
