# STIM300 Simulator

The STIM300 Simulator is a Python script that simulates data transmission for the STIM300 inertial measurement unit. It generates simulated datagrams based on user commands and communicates through a virtual serial port.


## Setup

1. **Clone the Repository:**
   
   git clone https://github.com/a1819644/ElementRobotics.git
   cd stim300-simulator

3. **Install dependencies:**
    ```pip install -r requirements.txt```

4. **Run the simulators**
    Note: make sure to change the port numbers 
    ```datagram.py```
    ```python stim300_guicp.py```
5. **How to operate Automode, NormalMode, ServiceMode**
    MUST: user needs to deactivate Automode when they would like to use Normal mode and vice versa for other mode testing 
    NOTE: depanding on the connect, I have faced the issue of the data delaying, so I would highly recommend my user to press normal mode operation button one more time or more if the screen isn't displaying data...
    TODO: I'm working on the issue to resolve it..