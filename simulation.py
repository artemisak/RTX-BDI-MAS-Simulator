import time
from datetime import datetime, timedelta

import numpy as np

from agents import Patient, Physician, Intern


class Simulator:
    start_time = datetime.now()
    physicians = []
    interns = []
    patients = []

    @staticmethod
    def generate_patients(intensity=5, time_span=30, size=1):
        last = Simulator.start_time
        for latency in np.round(np.random.exponential(scale=time_span / intensity, size=size)):
            last += timedelta(minutes=latency)
            Simulator.patients.append(Patient(income_time=last, available_physicians=Simulator.physicians))
            yield latency

    @staticmethod
    def generate_physicians():
        Simulator.physicians = [Physician(assistants=Simulator.interns) for _ in range(1, 5)]

    @staticmethod
    def generate_intern():
        Simulator.interns = [Intern() for _ in range(1, 11)]

    def run_simulation(self):
        self.generate_intern()
        self.generate_physicians()
        i = 0
        while i < 10:
            for latency in self.generate_patients():
                print('\n\n\n')
                for intern in self.interns:
                    print(intern.id, intern.role, intern.name, intern.efficiency)
                for physician in self.physicians:
                    print(physician.id, physician.role, physician.name,
                          physician.qualification, physician.workload,
                          [{i.id: i.name} for i in physician.pipeline],
                          [{i.id: i.name} for i in physician.completed])
                for patient in self.patients:
                    print(patient.id, patient.role, patient.name, patient.physician.id, patient.task.urgency,
                          patient.task.intricate, patient.income_time, patient.resume_time)
                i += 1
                if len(Simulator.patients) > 1:
                    time.sleep(latency / 10)

    def __init__(self, start_datetime=None):
        if start_datetime:
            Simulator.start_time = datetime.strptime(start_datetime,
                                                     '%d.%m.%Y %H:%M')
