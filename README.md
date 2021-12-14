# Magic Wand

This project utilizes a Wii remote to determine the flight path of a drone.

## File Description

- `data`: Data from each flight
   - `[date]-[time]-[defualt/custom]-ctrl-[default/custom]-obsv`: Flight date and time, and specified configuration
      -  `flight_video.mov`: User-uploaded video of the flight
      -  `gui.png`: Image of the gui after the flight 
      -  `hardware_data.json`: Data from the flight
-  `docs`: Documentation for this project, including project updates/reports
-  `src`: Source code to run the application
   -  `client.py`: Drone-interfacing class imported by the graphical user interface (GUI)
   -  `gui.py`: GUI for the user to control the drone
   -  `main.py`: Integrated file where application is executed
   -  `controller_ae483.c`: Custom controller and observer firmware
- `run_macos.sh`: Executable to run the application on MacOS
- `run_win.bat`: Executable to run the application on Windows
- `final-project.ipynb`: Jupyter Notebook analyzing the flights in different configurations

## Getting Started

### Dependencies

#### MacOS

* Required tools
    * Xcode command line tools
    * homebrew
    * Miniconda/Anaconda

Install the necessary tools using homebrew
```
brew install git-lfs
brew install libusb
brew tap PX4/homebrew-px4
brew install gcc-arm-none-eabi
```

Install the necessary Python packages using conda
```
conda install numpy scipy sympy matplotlib
pip install notebook
pip install cfclient
pip install cflib
pip install pybullet --no-cache-dir
pip install tk
pip install Pillow
```

### Download the code

Clone the firmware for drone
```
git clone --recursive https://github.com/tbretl/crazyflie-firmware.git
```

Clone control code from this repository
```
git clone https://github.com/ktt3/ae483-magic-wand.git
```

## Executing program

#### MacOS

Make the script executable (one time)
```
chmod +x run_macos.sh
```

Run the script in Terminal
```
./run_macos.sh
```

#### Windows

Run the script in Command Prompt
```
run_win.bat
```
## Authors

Erika Jarosch, George Petrov, Justin Roskamp, Kenneth Tochihara

## Acknowledgments

* [Professor Tim Bretl](https://aerospace.illinois.edu/directory/profile/tbretl)
* [AE 483 lab client codebase](https://github.com/tbretl/crazyflie-client)
* [AE 483 lab firmware codebase](https://github.com/tbretl/crazyflie-firmware.git)

