import json
import time
from datetime import datetime, timedelta
import numpy as np
from agents import Patient, Physician, Intern


class Simulator:
    start_time = datetime.now()
    last = datetime.now()
    physicians = []
    interns = []
    patients = []

    @staticmethod
    def generate_patients(intensity=5, time_span=30, size=1):
        latency = float(np.round(np.random.exponential(scale=time_span / intensity, size=size))[0])
        Simulator.last += timedelta(minutes=latency)
        Simulator.patients.append(Patient(income_time=Simulator.last, available_physicians=Simulator.physicians))
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
        while i < 100:
            for latency in self.generate_patients():
                with open('Results/intern.json', 'w') as file:
                    interns_data = []
                    for intern in self.interns:
                        print(f"{intern.id}, {intern.role}, {intern.name}, {intern.efficiency}\n")
                        intern_data = {
                            "id": intern.id,
                            "role": intern.role,
                            "name": intern.name,
                            "efficiency": intern.efficiency
                        }
                        interns_data.append(intern_data)

                    json.dump(interns_data, file)

                with open('Results/physician.json', 'w') as file1:
                    physicians_data = []
                    for physician in self.physicians:
                        print(f"""{physician.id}, {physician.role}, {physician.name}, {physician.qualification},
                              {physician.workload}, {[{i.id: i.name} for i in physician.pipeline]},
                              {[{i.id: i.name} for i in physician.completed]}\n
                              """)
                        physician_data = {
                            "id": physician.id,
                            "role": physician.role,
                            "name": physician.name,
                            "qualification": physician.qualification,
                            "workload": physician.workload,
                            "_pipeline": [{i.id: i.name} for i in physician.pipeline],
                            "completed": [{i.id: i.name} for i in physician.completed]
                        }
                        physicians_data.append(physician_data)

                    json.dump(physicians_data, file1)

                with open('Results/patient.json', 'w') as file2:
                    patients_data = []
                    for patient in self.patients:
                        print(f"""{patient.id}, {patient.role}, {patient.name}, {patient.physician.id},
                                  {patient.task.urgency}, {patient.task.intricate}, {patient.income_time},
                                  {patient.resume_time}\n
                               """)
                        patient_data = {
                            "id": patient.id,
                            "role": patient.role,
                            "name": patient.name,
                            "physician_id": patient.physician.id,
                            "urgency": int(patient.task.urgency),
                            "intricate": int(patient.task.intricate),
                            "income_time": f"{patient.income_time}",
                            "resume_time": f"{patient.resume_time}"
                        }
                        patients_data.append(patient_data)

                    json.dump(patients_data, file2)

                i += 1
                if len(Simulator.patients) > 1:
                    time.sleep(latency / 10)

    def __init__(self, start_datetime=None):
        if start_datetime:
            Simulator.start_time = datetime.strptime(start_datetime,
                                                     '%d.%m.%Y %H:%M')
