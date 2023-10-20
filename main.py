import datetime
import numpy as np


class Simulator:
    patients = []
    physicians = []

    def generate_patients(self, intensity=5, time_span=30, size=10):
        last = self.start_time
        for latency in np.round(np.random.exponential(scale=time_span / intensity, size=size)):
            last += datetime.timedelta(minutes=latency)
            Simulator.patients.append(Patient(income_time=last))

    def generate_physicians(self):
        Simulator.physicians = [Physician() for _ in range(1, 5)]

    def __init__(self, start_now=True, start_date='17.10.2023 9:00'):
        if start_now:
            self.start_time = datetime.datetime.now()
        else:
            self.start_time = datetime.datetime.strptime(start_date,
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

    def update_efficiency(self):
        self.efficiency = self.successes / self.attempts


class Physician(Agent):

    def __init__(self):
        super().__init__(role='Physician')
        self.qualification = np.random.choice(['Doctor of Medical Sciences',
                                               'Candidate of Medical Sciences',
                                               'Specialist'], p=[0.2, 0.3, 0.5])
        self.pipeline = []
        self.completed = []
        self._workload = 0

    @property
    def workload(self):
        return len(self.pipeline)

    def assign(self, value):
        self.pipeline.append(value)

    def release(self, value):
        idx = self.pipeline.index(value)
        self.completed.append(self.pipeline.pop(idx))


class Patient(Agent):

    def __init__(self, income_time):
        super().__init__(role='Patient')
        self.income_time = income_time
        self.resume_time = None
        self.task = Task()
        self.physician = None

    def choose_physician(self):
        executor = np.random.choice(Simulator.physicians)
        self.physician = executor
        executor.assign(value=self)


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
    instance.generate_patients()
    instance.generate_physicians()

    for patient in instance.patients:
        patient.choose_physician()
        print(patient.id, patient.role, patient.name, patient.physician.id, patient.task.urgency,
              patient.task.intricate)
    fun = lambda x: [i.id for i in x]
    for physician in instance.physicians:
        print(physician.id, physician.role, physician.name,
              physician.qualification, physician.workload,
              fun(physician.pipeline))
