<p align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Documentation-logo.svg"/>
</p>

<h1>Table of contents</h1>

  - [Agents](#agents)
    - [Base class](#base-class)
    - [Patient](#patient)
    - [Physician](#physician)
    - [Intern](#intern)
  
<h1>Agents</h2>

The Agents file contains the classes of all agents involved in the clinic's life process. 

<h2>Base class</h3>

First of all, let's consider the ```BaseAgent``` abstract class, which is the base class for all other classes.

```python
class BaseAgent:
    id = 0
    _surnames = config["NAMES"]["LAST_NAMES"].split(sep=', ')
    _first_names = config["NAMES"]["FIRST_NAMES"].split(sep=', ')

    def __init__(self, role):
        self.id = BaseAgent.id
        BaseAgent.id += 1
        self.role = role
        self.name = " ".join([np.random.choice(self._first_names), np.random.choice(self._surnames)])
```

It has a static ```id``` field, which is shared between all instances of the class and is incremented by 1 when a descendant is initialized.

In addition, ```BaseAgent``` contains two more static fields ```_surnames``` and ```_first_names```, reflecting the available sets of first and last names to generate the full name stored in the ```name``` field and forming a unique combination together with ```id```. The first and last names are not stored directly in the python code, instead we use a configuration file.

The BaseAgent initializer contains a ```role``` variable, which is then assigned to a field of the same name. The ```role`` is what defines the conduct of the agent in the simulator logic. Roles are of 3 types: patient, physician, and intern.

<h2>Patient</h3>

```python

class Patient(BaseAgent):

    @staticmethod
    def createTask():
        return Task()

    def choosePhysician(self, pool):
        physician = np.random.choice(pool)
        thread = threading.Thread(target=physician.request_handler, args=(self,))
        thread.start()
        return physician

    def __init__(self, income_time, available_physicians):
        super().__init__(role='Patient')
        self.income_time = income_time
        self.resume_time = None
        self.task = self.createTask()
        self.physician = self.choosePhysician(pool=available_physicians)

```

<h2>Physician</h3>

<h2>Intern</h3>
