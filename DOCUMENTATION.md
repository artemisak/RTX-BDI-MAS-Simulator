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

<h3>Field Types</h3>

| Field | Type |
|-------|------|
|```id```|```Int```|
|```role```|```String```|
|```_surnames```|```[String]```|
|```_first_names```|```[String]```|
|```name```|```String```|

<h3>Method Types</h3>

| Method | Input | Output |
|-------|------|------|
|```init()```|```role``` : ```String```|```BaseAgent```|

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

Last, consider the ```resume_time``` field. The field is declared and initialized with a None value. The field is populated after ```physician.request_handler()``` is successfully executed.

<h3>Field Types</h3>

| Field | Type |
|-------|------|
|```income_time```|```datetime```|
|```resime_time```|```None``` / ```datetime```|
|```task```|```Task```|
|```physician```|```Physician```|


<h3>Method Types</h3>

<table>
  <thead>
    <th>Method</th>
    <th>Input</th>
    <th>Output</th>
  </thead>
  <tbody>
    <tr>
      <td rowspan=2><code>init()</code></td>
      <td><code>incometime</code> : <code>datetime</code></td>
      <td rowspan=2><code>Patient</code></td>
    </tr>
    <tr>
        <td><code>available_physicians</code> : <code>[Physician]</code></td>
    </tr>
    <tr>
      <td><code>createTask()</code></td>
      <td align="center">-</td>
      <td><code>Task</code></td>
    </tr>
    <tr>
      <td><code>choosePhysician()</code></td>
      <td><code>pool</code> : <code>[Physician]</code></td>
      <td><code>Physician</code></td>
    </tr>
  </tbody>
</table>

<h2>Physician</h3>

The ```Physician``` class describes the basic properties of a radiologist in the agent chain of a multi-agent system.

```python
class Physician(BaseAgent):

    @property
    def workload(self):
        return len(self.pipeline)

    @staticmethod
    def choose_intern(pool):
        return np.random.choice(pool)

    def request_handler(self, request):
        self.assign(request)
        self.solve(request, self.assistants)
        self.release(request)

    def assign(self, objective):
        self.pipeline.append(objective)

    def solve(self, objective, assistants):
        intern = self.choose_intern(assistants)
        result = 0
        latency = timedelta(minutes=0)
        while result == 0:
            outcome = intern.generate_outcome(objective.task)
            result = outcome.result
            if result == 0:
                latency = (timedelta(minutes=outcome.time) +
                           timedelta(minutes=int(np.random.choice([x for x in range(1, 4)]))))
            else:
                latency = (timedelta(minutes=outcome.time) +
                           timedelta(minutes=int(np.random.choice([x for x in range(7, 10)]))))
        objective.resume_time = objective.income_time + latency
        time.sleep(int(latency.total_seconds() / 600))

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
        self.pipeline = []
        self._workload = 0
```

Each radiologist has inherent properties: the degree of medical training, expressed by the variable ```qualification```, and the set of residents with whom he cooperates, expressed by the variable ```assistants```.

When a patient's request is received, the ```request_handler()``` method starts executing, which includes three steps:

 - ```assign()``` - adding the patient to the ```pipeline```;

 - ```solve()``` - reading the MRI image, making a diagnosis and prescribing therapy, in this case, one of the available interns is selected for MRI image markup using the web-based image markup platform developed by us;

 - ```release()``` - extracting the patient from the current ```pipeline``` and adding it to the solved cases expressed by the ``completed`` variable.

The computational field ```workload``` reflects the length of the working ```pipeline``` at the current time. The property can be called at any time to document the state of the agent.

<h3>Field Types</h3>

| Field | Type |
|-------|------|
|```qualification```|```String```|
|```assistants```|```[Intern]```|
|```completed```|```[Patient]```|
|```pipeline```|```[Patitent]```|
|```workload```|```Int```|

<h3>Method Types</h3>

<table>
  <thead>
    <th>Method</th>
    <th>Input</th>
    <th>Output</th>
  </thead>
  <tbody>
    <tr>
      <td>
        <code>init()</code>
      </td>
      <td>
        <code>assistants</code> : <code>[Intern]</code>
      </td>
      <td>
        <code>Physician</code>
      </td>
    </tr>
    <tr>
      <td>
        <code>choose_intern()</code>
      </td>
      <td>
        <code>pool</code> : <code>[Intern]</code>
      </td>
      <td>
        <code>Intern</code>
      </td>
    </tr>
    <tr>
      <td>
        <code>request_handler()</code>
      </td>
      <td>
        <code>request</code> : <code>Patient</code>
      </td>
      <td align="center">
        -
      </td>
    </tr>
    <tr>
      <td>
        <code>assign()</code>
      </td>
      <td>
        <code>objective</code> : <code>Patient</code>
      </td>
      <td align="center">
        -
      </td>
    </tr>
    <tr>
      <td rowspan=2>
        <code>solve()</code>
      </td>
      <td>
        <code>objective</code> : <code>Patient</code>
      </td>
      <td rowspan=2 align="center">
        -
      </td>
    </tr>
    <tr>
      <td>
          <code>assistants</code> : <code>[Intern]</code>
      </td>
    </tr>
    <tr>
      <td>
        <code>release()</code>
      </td>
      <td>
        <code>objective</code> : <code>Patient</code>
      </td>
      <td align="center">
        -
      </td>
    </tr>
  </tbody>
</table>

<h2>Intern</h3>
