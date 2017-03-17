## RProtocolBackend
This repository will hold the code for the RELION backend. Eventually, we will move to a client-server architecture, where the 
server is responsible for scheduling, organizing, and executing the user-submitted jobs. The users will
submit jobs using a graphical frontend (hosted in a different repository).

For now, the RELION project directory parsing code and automated job execution code will be held here without having
server capabilities. Later in the process, job submission and job querying capabilities will be added in the form of a RESTful API to
this project (along with creating the GUI in a different repository).