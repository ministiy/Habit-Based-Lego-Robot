# Summer Research Project - Supervised by Matthew Egbert

## Setting up
Connecting to the robot using Server/Client Socket. With the robot as the client, and desktop as the server.\
For wired setup, go to [Wired Setup](http://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/)\
For wireless setup, go to [Wireless Setup](WirelessSetup.md)

Note: It is **much better** to use dualboot since there are no added complexity, but using VirtualBox will also works with the right setup.

## Transfer file from desktop to ev3dev robot
If you want to move files from your desktop to the robot:
1. Find the robot IP address on the top left side of the ev3dev robot.
2. SSH to the robot [via USB cable](http://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/) or [via Wi-Fi](WirelessSetup.md)
3. Open another terminal, and run ***scp /path/to/file robot@robot's IP address:/path/to/destination***
4. Put the password when asked; default password is **maker**
5. If you want to execute the files from the robot directly without SSH, run ***chmod +x /path/to/file*** when you are connected to the robot through SSH

## Establishing a Client-Server connection between robot and computer
1. Make sure you have the following files on the **computer**. They should be in the same directory.
* **SocketServer.py** - The "server" script
* **writeCSV.py** - Used to write data to a CSV file
* **Constant.py** - Holds important shared constants between client and server machines
* **stopmotors.sh** - A bash script to stop motors in the event that they do not stop

2. Make sure you have the following Python files on the **robot**. They should be in the same directory.
* **SocketClient.py**
* **Ev3devSetup.py**
* **Constant.py**

3. Execute the **SocketServer.py** script in terminal. Use Python 3. (**python3 SocketServer.py**)
4. Execute the **SocketClient.py** script. There are two main ways to execute the **SocketClient.py**:
* **Via SSH** - SSH to the robot, navigate to where **SocketClient.py** is located and execute it. Use Python 3.
* **Via the robot itself** - Using the Mindstorms brick screen, you should be able to navigate through the file system on the robot. Execute the file by selecting **SocketClient.py**.

5. 
