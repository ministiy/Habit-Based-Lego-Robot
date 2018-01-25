# Summer Research Project - Supervised by Matthew Egbert

## Setting up
Connecting to the robot using Server/Client Socket. With the robot as the client, and desktop as the server.\
For wired setup, go to [Wired Setup](http://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/)\
For wireless setup, go to [Wireless Setup](WirelessSetup.md)

Note: It is **much better** to use dualboot since there are no added complexity, but using VirtualBox will also works with the right setup.

## Transfer file from desktop to ev3dev robot
If you want to move files from your desktop to the robot:
1. Find the robot IP address on the top left side of the ev3dev robot.
2. SSH to the robot [Wired](http://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/) or wirelessly as explained in [Wireless Setup](WirelessSetup.md)
3. Open another terminal, and run ***scp /path/to/file robot@robot's IP address:/path/to/destination***
4. Put the password when asked, default is **maker**
5. If you want to execute the files from the robot directly without SSH, run ***chmod +x /path/to/file*** when you are connected to the robot through SSH


