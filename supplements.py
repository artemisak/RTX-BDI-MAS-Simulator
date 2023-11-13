import numpy as np


class Result:
    def __init__(self, success_rate, mean_time, std):
        self.result = np.random.choice([0, 1], p=[1 - success_rate, success_rate])
        self.time = np.random.normal(mean_time, std)


class Task:
    def __init__(self):
        self.urgency = np.random.choice([1, 2, 3], p=[.6, .3, .1])
        self.intricate = np.random.choice([True, False], p=[.3, .7])
