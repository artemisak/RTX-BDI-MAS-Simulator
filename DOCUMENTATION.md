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

The ```Patient``` сlass reflects a person, with some hidden set of physiological parameters, implicitly expressed by the ```Task``` he or she sets for the doctor to investigate.

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

Once we note that before declaring and initializing with some values the fields of the ```BaseAgent``` descendant class, it is necessary to initialize the parent class, assigning the agent the appropriate role, in this case the role of 'Patient'.

```python
super().__init__(role='Patient')
```

Subsequently, this step will be repeated when initializing the ```Physician``` and ```Intern``` classes.

The patient initializer takes two variables as input: the time the request was received, expressed by the ```income_time``` variable, and the pool of radiology physicians available for selection in the ```available_physicians``` variable. 

The ```task``` field is initialized by an instance of the ```Task``` class. To get the corresponding instance, you need to call the ```CreateTask()``` method. It is assumed that the real life task can be obtained using more complex logic, including using GAN tools to generate the most rare and missing samples of the ```Task``` class.

The ```physician``` field is filled in according to the results of the ```choosePhysician()``` function. This method randomly returns a physician from the list of available physicians and starts a separate subprocess to perform the received objective using the methods of the built-in library ```threading```.

It is important that the argument of the ```physician.request_handler()``` function is directly an instance of the ```Patient``` class, which is reflected in this line.

```python
thread = threading.Thread(target=physician.request_handler, args=(self,))
```

<h2>Physician</h3>

<h2>Intern</h3>
