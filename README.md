# Magic Wand

This project utilizes a Wii remote to plan the path of a drone.

## Description

An in-depth paragraph about your project and overview of use.

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

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Authors

Erika Jarosch, George Petrov, Justin Roskamp, Kenneth Tochihara

## Acknowledgments

* [Professor Tim Bretl](https://aerospace.illinois.edu/directory/profile/tbretl)
* [AE 483 lab client codebase](https://github.com/tbretl/crazyflie-client)
* [AE 483 lab firmware codebase](https://github.com/tbretl/crazyflie-firmware.git)

