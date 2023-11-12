<div align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Logo.svg">
</div>

<div>
  
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org/)
[![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=whit)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white)](https://scipy.org/)
[![Node.js](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/express.js-%23404d59.svg?style=for-the-badge&logo=express&logoColor=%2361DAFB)](https://expressjs.com/)

</div>

<h1>Installation</h1>

The following set of dependencies will need to be installed for the simulation to work:

```
sudo apt update
sudo apt install nodejs npm python3
```

Then navigate to the ```web/client``` and ```web/server``` folders to install the dependencies from ```package.json``` necessary to run the web application that outputs the simulation results as tables. Skip this step if visualization is not required.

Once in the desired directory, you can use the following command:

```
npm install
```

In addition, you will need to install program modules to run the simulation code directly:

```
python -m pip install numpy scipy
```

<h1>Usage</h1>

To run the simulation, you must first start the web application in developer mode. To do this, go to the ```web/client``` directory and start the server responsible for the frontend.

```
npm run dev
```

The frontend of the app will be available at ```http://localhost:3000/```.

The application backend is launched using a similar command from the ```web/server``` directory.

```
npm run start
```

Note that when you start the server, the ```nodemon``` startup notification appears.
This means that a process has been started to track changes to the ```/Results directory```. The ```/Results``` directory contains several JSON files that are populated with the simulator results. Beckend uses Server-Send-Events (SSE) technology to track changes to ```/Results``` and reflect them to the frontend in a timely manner.

To run the simulation process that populates the JSON files, go to the root directory and run the ```/main.py``` file.

```
python main.py
```

Once these steps are completed, the simulation will start running and the results will be dynamically reflected at ```http://localhost:3000/```.

<h1>Caution</h1>

For best experience, make sure JSON files are created and empty. Also, after stopping the simulation and closing the application, make sure in the task manager that all running Node JS processes are actually stopped. There have been cases where ```nodemon``` continues to execute its process despite the main process being terminated. If this happens, the next time you run the application you will get an error stating that the ```nodemon``` process is already running.

<h1>Documentation</h1>

Read the detailed documentation of how the simulation program code works [here](https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/DOCUMENTATION.md).
 
<h1>Theoretical basis</h1>

The general structure of the modelling process is outlined below. We use an exponential distribution with a scale of 1/lambda to generate the time between occurring events. An event is the appearance of a patient, which is characterised by several parameters: the time of the request appearance, the time of service provision, the task assigned and the selected doctor. From the point of view of RTX-BDI-MAS, patients act as agents, because by choosing a doctor from the list of available ones, they assign a task, i.e. they participate in the management of clinic resources. The best way to modify the policy of user behavior as agents is to study user behavior on the site and optimize search results (for example, a list of doctors) according to the degree of compliance of the qualification and the area of the stated task.

A task is a certain MRI image to be decoded. The task, like the patient, is a named entity and has the following parameters: urgency and complexity. Urgency can take values from 1 to 3, where 1 is an urgent task (hospitalisation, severe condition), 2 is a task of medium urgency (the patient is conscious, injuries of no more than medium severity), 3 is the lowest priority (regular examinations, monitoring, minor injuries). Complexity is evaluated by a binary variable, either the task requires the highest qualification of a specialist or it does not. Complexity is a linear combination of technical complexity in image processing and urgency of the task. Thus, even tasks with the lowest priority can be considered as complex if they require more than usual processing time. The decision and complexity of the problem can be taken by a feed forward propagation neural network. For simulation purposes, its work is replaced by a random number generator. But in real RTX-BDI-MAS work, pre-scanning an image to assign it to one of two complexity categories has the potential to facilitate informed decision making in the process of matching available resources and agents in the clinic network.

<div align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Simulation_graph.svg"/>
</div>

It is worth mentioning that the available specialists are both agents and the main human resource of the clinic. Physicians are the specialists whose job it is to decipher the MRI image. They are assisted by interns who mark up the images. First of all, a doctor is characterised by his/her qualification, which can be assessed on a scale from 1 to 3, where 1 is a Doctor of Medical Sciences, 2 is a Candidate of Medical Sciences, and 3 is a specialist. During the simulation, the same doctor may receive several requests, similar to a live queue. The length of this queue is called the workload. From the point of view of RTX-BDI-MAS, this parameter can be used to predict the approximate waiting time before the start of a new task. And, consequently, optimisation of workload will reduce the average waiting time for the execution of a request in the network.

Interns are aspiring doctors who have received proper education, but have not completed the appropriate course of live practice. They are characterized by the chance of success, the time to complete the task efficiency. For simulation purposes, the task execution time is randomly selected from the normal distribution. More successful interns have, on average, a shorter task completion time and a greater chance of completing the task the first time. The simulation uses a hierarchical criterion. In order for the task to be considered completed, it must be accepted by a more senior medical officer. Otherwise, inter spends extra time on redoing. The intern's work efficiency is characterized as the ratio of the number of successfully completed tasks to the total number of tasks for the allocated period of time. From the point of view of RTX-BDI-MAS, the efficiency of each inter should be maximized, for which less successful inters can be assigned easier tasks, while the most effective ones are complex. As an intern accumulates experience, the chances of successfully completing previously studied tasks tend to increase, which gives rise to a reassessment of the resource management policy. Thus, it is advisable to allocate a new type of tasks to an intern, which he has not previously encountered, to the detriment of his momentary efficiency, but to increase it in the medium and long term. In the RTX-BDI-MAS system, where people act as agents, training is seen as the most effective way to modify the agent's policy, since we cannot change the agent's implicit parameters forcibly.

Below are screenshots of the results of running the simulation. A tiny web application with Server-Sent Events (SSE) support was developed for this purpose. In addition to tables, the application logs the process as the simulation progresses and outputs intermediate changes to the terminal.

The patient table contains the information necessary to identify the user and his/her task, also the time interval of the patient's stay in the state of waiting for the doctor's decision.

<div align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Patients_table.svg"/>
</div>

The table of doctors contains information about the state in which the doctor is at the moment of the last iteration of the simulator operation. It reflects the current workload, the list of patients waiting for a decision and the history of visits of this doctor.

<div align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Physicians_table_1.svg"/>
</div>

<div align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Physicians_table_2.svg"/>
</div>

The interns table reflects only the visible and measurable attributes of this type of agent. Implicit attributes, remain hidden.

<div align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Interns_efficiency_table.svg"/>
</div>

The proposed block diagram of RTX-BDI-MAS operation in the form of an acyclic directed graph is presented below.  The loss function we aim to minimize is the product of the average waiting time in the queue and the sufficiency of the medical decision, which is defined inversely by the physician's qualification (3 - insufficient, 2 - more than sufficient, 1 - sufficient). Thus, we aim to minimize the average waiting time using the minimum necessary and sufficient physician qualifications.

<p align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Acyclic_oriented_graph.svg"/>
</p>
