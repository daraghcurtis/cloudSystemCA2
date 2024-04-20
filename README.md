# Cloud Systems CA2 DCU (Mininet & Remote floodlight controller

## Introduction
This is a college MiniNet (SDN) CA which uses floodlight as the Controller

## Requirements
1.Floodlight is running in a separate remote VM <br>
2.You have vitualbox installed on your machine <br>
3.You have mininet installed on your machine <br>


## Installation
Best way is to clone the project to your local mininet machine custom folder <br>
`git clone https://github.com/daraghcurtis/cloudSystemCA2.git` <br>

Otherwise you can copy the files to the custom folder on the mininet VM : <br>
*On your miniNet VM :* <br>

1. Go to the mininet custom folder on the mininet VM <br>
e.g here : `mininet@mininet-vm:~/mininet/custom` <br>
2. create a file called `topo_v2.py` by doing `nano topo_v2.py` <br>
3. copy the content from git repo file `topo_v2.py` to the new VM file `topo_v2.py` file
3. Change the IP address in the file to the IP address of the remote VM where floodlight is running  
*lines 14 - 15*   
Example :   <br>
```
ip='192.168.147.62' # Ip address of floodlight server 
port=6653 # Remote controller port listening on floodlight
```
4. save the file : `ctl+x, y, enter`

## Running the code
5. Run the following commands in the mininet VM from custom folder where you created the py file : <br>
```
sudo mn --c <br> 
sudo python topo_v2.py 
``` 
<br>

## Testing
The test cases will automatically run when the code is run. <br>
If a test fails, mininet will exit so that you can see the issue. <br>

## Exit miniNet
To exit mininet, type `exit` or press `ctrl + d`
