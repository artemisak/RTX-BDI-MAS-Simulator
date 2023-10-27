# RTX-BDI-MAS Simulator

The general structure of the modelling process is outlined below. We use an exponential distribution with a scale of 1/lambda to generate the time between occurring events. An event is the appearance of a patient, which is characterised by several parameters: the time of the request appearance, the time of service provision, the task assigned and the selected doctor. From the point of view of RTX-BDI-MAS, patients act as agents, because by choosing a doctor from the list of available ones, they assign a task, i.e. they participate in the management of clinic resources. The best way to modify the policy of user behavior as agents is to study user behavior on the site and optimize search results (for example, a list of doctors) according to the degree of compliance of the qualification and the area of the stated task.

A task is a certain MRI image to be decoded. The task, like the patient, is a named entity and has the following parameters: urgency and complexity. Urgency can take values from 1 to 3, where 1 is an urgent task (hospitalisation, severe condition), 2 is a task of medium urgency (the patient is conscious, injuries of no more than medium severity), 3 is the lowest priority (regular examinations, monitoring, minor injuries). Complexity is evaluated by a binary variable, either the task requires the highest qualification of a specialist or it does not. Complexity is a linear combination of technical complexity in image processing and urgency of the task. Thus, even tasks with the lowest priority can be considered as complex if they require more than usual processing time. The decision and complexity of the problem can be taken by a feed forward propagation neural network. For simulation purposes, its work is replaced by a random number generator. But in real RTX-BDI-MAS work, pre-scanning an image to assign it to one of two complexity categories has the potential to facilitate informed decision making in the process of matching available resources and agents in the clinic network.

<p align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/simulation-graph.svg"/>
</p>

It is worth mentioning that the available specialists are both agents and the main human resource of the clinic. Physicians are the specialists whose job it is to decipher the MRI image. They are assisted by interns who mark up the images. First of all, a doctor is characterised by his/her qualification, which can be assessed on a scale from 1 to 3, where 1 is a Doctor of Medical Sciences, 2 is a Candidate of Medical Sciences, and 3 is a specialist. During the simulation, the same doctor may receive several requests, similar to a live queue. The length of this queue is called the workload. From the point of view of RTX-BDI-MAS, this parameter can be used to predict the approximate waiting time before the start of a new task. And, consequently, optimisation of workload will reduce the average waiting time for the execution of a request in the network.

Interns are aspiring doctors who have received proper education, but have not completed the appropriate course of live practice. They are characterized by the chance of success, the time to complete the task efficiency. For simulation purposes, the task execution time is randomly selected from the normal distribution. More successful interns have, on average, a shorter task completion time and a greater chance of completing the task the first time. The simulation uses a hierarchical criterion. In order for the task to be considered completed, it must be accepted by a more senior medical officer. Otherwise, inter spends extra time on redoing. The intern's work efficiency is characterized as the ratio of the number of successfully completed tasks to the total number of tasks for the allocated period of time. From the point of view of RTX-BDI-MAS, the efficiency of each inter should be maximized, for which less successful inters can be assigned easier tasks, while the most effective ones are complex. As an intern accumulates experience, the chances of successfully completing previously studied tasks tend to increase, which gives rise to a reassessment of the resource management policy. Thus, it is advisable to allocate a new type of tasks to an intern, which he has not previously encountered, to the detriment of his momentary efficiency, but to increase it in the medium and long term. In the RTX-BDI-MAS system, where people act as agents, training is seen as the most effective way to modify the agent's policy, since we cannot change the agent's implicit parameters forcibly.

Below are screenshots of the results of running the simulation. A tiny web application with Server-Sent Events (SSE) support was developed for this purpose. In addition to tables, the application logs the process as the simulation progresses and outputs intermediate changes to the terminal.

The patient table contains the information necessary to identify the user and his/her task, also the time interval of the patient's stay in the state of waiting for the doctor's decision.

<p align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Patients_table.png"/>
</p>

The table of doctors contains information about the state in which the doctor is at the moment of the last iteration of the simulator operation. It reflects the current workload, the list of patients waiting for a decision and the history of visits of this doctor.

<p align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Physicians_table.png"/>
</p>

The interns table reflects only the visible and measurable attributes of this type of agent. Implicit attributes, remain hidden.

<p align="center">
  <img src="https://github.com/artemisak/RTX-BDI-MAS-Simulator/blob/main/Supplements/Interns_table.png"/>
</p>
