# Cloud Systems CA2 DCU (Mininet & Remote floodlight controller

## Introduction
This is a college MiniNet (SDN) CA which uses floodlight as the Controller

## Requirements
Floodlight is running in a separate remote VM <br>
You have vitualbox installed on your machine <br>
You have mininet installed on your machine <br>


## Installation
Best way is to clone the project to your local mininet machine custom folder <br>
`https://github.com/daraghcurtis/cloudSystemCA2.git` <br>

Else you can copy the files to the custom folder on the mininet VM <br>

Go to the mininet custom folder on the mininet VM <br>
e.g here : <br> `mininet@mininet-vm:~/mininet/custom`

<br>
create a file called `topo_v2.py` by doing `nano topo_v2.py` <br>
<br>copy the code from the `topo_v2.py` file

Change the IP address in the file to the IP address of the remote VM where floodlight is running  
**lines 14 - 15**   
Example :   <br>
`ip='192.168.147.62' # Ip address of floodlight server`  
`port=6653 # Remote controller port listening on floodlight`
<br> save the file : `ctl+x, y, enter`

## Running the code
Run the following commands in the mininet VM from custom folder where you created the py file : <br>
`sudo mn --c` <br>
`sudo python topo_v2.py` <br>

## Testing
The test cases will automatically run when the code is run. <br>
If a test fails, mininet will exit so that you can see the issue. <br>

## Exit miniNet
To exit mininet, type `exit` or press `ctrl + d`
