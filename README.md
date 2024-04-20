# Cloud Systems CA2 DCU (Mininet & Remote floodlight controller

## Introduction
This is a college MiniNet (SDN) CA which uses floodlight as the Controller

## Requirements
Floodlight is running in a separate remote VM
You have vitualbox installed on your machine
You have mininet installed on your machine


## Installation
Go to the mininet custom folder  
e.g here : `mininet@mininet-vm:~/mininet/custom`

On the mininet VM :   
create a file called `topo_v2.py` and copy the code from the `topo_v2.py` file in this file  
by doing `nano topo_v2.py`  
change the IP address in the file to the IP address of the remote VM where floodlight is running  
lines 14 - 15   
Example :   
`ip='192.168.147.62' # Ip address of floodlight server`  
`port=6653 # Remote controller port listening on floodlight`

save the file : ctl+x, y, enter

## Running the code
Run the following commands in the mininet VM:  

## Testing
The test cases will automatically run when the code is run

## Exit miniNet
To exit mininet, type `exit` or press `ctrl + d`
