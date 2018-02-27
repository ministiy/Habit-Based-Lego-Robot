# Summer Research Project - Supervised by Matthew Egbert

## Setting up
Connecting to the robot using Server/Client Socket. With the robot as the client, and desktop as the server.\
For wired setup, go to [Wired Setup](http://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/)\
For wireless setup, go to [Wireless Setup](WirelessSetup.md)

Note: It is **much better** to use dualboot since there are no added complexity, but using VirtualBox will also works with the right setup.

## How to run the client-server 
Setting up and running the client-server setup can be done by following the [tutorial](HOWTO.md).

## Folders

    server: folder containing files to be able to run the server on the computer side.
    client: folder containing files to be able to run the robot and connect to the server.
    res: folder containing images for documentation.
    jupyter: folder containing jupyter notebooks for data visualization.
    experiment: folder containing csv, photo and sketch of robot running in controlled environment with different initial position

## Livetrack robot values to Jupyter
1. Go to jupyter folder and run **jupyter notebook** in terminal.
2. Open the notebook in jupyter localhost that is opened in your browser
3. Start the robot with the client-server scripts.
4. Run the jupyter cell that you want to see the result of.
5. See the graph update automatically.
