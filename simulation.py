import time
from datetime import datetime, timedelta

import numpy as np

from agents import Patient, Physician


class Simulator:
    start_time = datetime.now()
    patients = []
    physicians = []

    @staticmethod
    def generate_patients(intensity=5, time_span=30, size=1):
        last = Simulator.start_time
        for latency in np.round(np.random.exponential(scale=time_span / intensity, size=size)):
            last += timedelta(minutes=latency)
            Simulator.patients.append(Patient(income_time=last, available_physicians=Simulator.physicians))

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
            Simulator.start_time = datetime.strptime(start_datetime,
                                                     '%d.%m.%Y %H:%M')
