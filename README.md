# A Simple python script to run VMware Workstation and EVE-NG using their API

NOTE: Scripts are not yet clean and might still have errors, since I'm still working on it. Script is not tested on the paid versions of VMware player and EVE-NG Pro.

The VMware script does not yet check if the API has been setup already, Use this [link](https://www.starwindsoftware.com/blog/how-does-rest-api-work-in-vmware-fusion-and-vmware-workstation) to know how to set it up.
The scripts on this repository is not that good so if you are looking for a more clean and better scripts for VMware and EVE-NG, might as well check the other ones. Since I wrote this scripts to help me learn more and improved my python skills and at the same time help me automate starting up my labs on EVE-NG

My end goal is to complete some To do comments on the scripts and combine the 2 scripts for me to just execute just 1 script.



## Will continue to update this doc once the 2 scripts has been combine

Sample script functions:
$ python Test_EVE-NG.py -d
Using default IP and Credentials
User logged in (90013).

Here are your folders and labs:
The folder "MyLabs" has the ff labs: ['test_lab']
The folder "TestLab" has the ff labs: ['MPLS', 'OSPF LAB', 'OSPFwIP', 'Test1']

Enter the lab name, you want to work on: test_lab

Here are the nodes on the lab: (Name - Image - ID)
  vIOS1 - vios-adventerprisek9-m.SPA.156-1.T - 1
  vIOS2 - vios-adventerprisek9-m.SPA.156-1.T - 2
  vIOS3 - vios-adventerprisek9-m.SPA.156-1.T - 3
  vIOS4 - vios-adventerprisek9-m.SPA.156-1.T - 4

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 1

==================================================

Starting all nodes:

All nodes['vIOS1', 'vIOS2', 'vIOS3', 'vIOS4'] has been started!

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 7

==================================================

Stopping all nodes:

All nodes ['vIOS1', 'vIOS2', 'vIOS3', 'vIOS4'] has been stopped!

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 2

==================================================

Starting vIOS1 with node id of 1:

vIOS1 had started

Starting vIOS2 with node id of 2:

vIOS2 had started

Do you want to start the remaining nodes? (y/n): n

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 7

==================================================

Stopping all nodes:

All nodes ['vIOS1', 'vIOS2', 'vIOS3', 'vIOS4'] has been stopped!

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 4

==================================================
The lab (test_lab.unl) has 4 nodes

Enter the number of nodes you want to start, or type (back) to return on the menu: 3

Starting ['1', '2', '3', '4'] nodes:
vIOS1 had started
vIOS2 had started
vIOS3 had started
The lab (test_lab.unl) has 4 nodes

Enter the number of nodes you want to start, or type (back) to return on the menu: back

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 6

==================================================

Enter the node names separated by space or comma. input 'back' to go back on the menu: vIOS1 vIOS2, vIOS3

Stopping node vIOS1:

vIOS1 has been stopped

Stopping node vIOS2:

vIOS2 has been stopped

Stopping node vIOS3:

vIOS3 has been stopped

Enter the node names separated by space or comma. input 'back' to go back on the menu: back

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 3

==================================================

Enter the node names separated by space or comma. input 'back' to go back on the menu: vIOS1, vIOS2 vIOS3

Starting node vIOS1:

vIOS1 had started

Starting node vIOS2:

vIOS2 had started

Starting node vIOS3:

vIOS3 had started

Enter the node names separated by space or comma. input 'back' to go back on the menu: back

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 5

==================================================
Node vIOS1 is currently Active with telnet IP/Port: 192.168.85.128:32769
Node vIOS2 is currently Active with telnet IP/Port: 192.168.85.128:32770
Node vIOS3 is currently Active with telnet IP/Port: 192.168.85.128:32771
Node vIOS4 is Not Active

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: 7

==================================================

Stopping all nodes:

All nodes ['vIOS1', 'vIOS2', 'vIOS3', 'vIOS4'] has been stopped!

==================================================
 Select an option how to proceed:
            1 = Start All nodes
            2 = Start half of the nodes
            3 = Start the nodes by using name
            4 = Start a number of nodes
            5 = List active nodes and their Telnet IP(Work in progress to replace option to open nodes cli on terminal)
            6 = Stop a node by using name
            7 = Stop all nodes on a lab
            8 = Change folder
            Q = Quit/Logout EVE-NG

            Please enter your choice: q

==================================================
Session Terminated
