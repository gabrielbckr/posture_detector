# Posture Detector

The project contains two source codes.

One is a python package, provided in
`posture_detector` directory. It has
tool functions for EDA, modelling,
model evaluation, ETL, parsing data, 
column constants etc.
It also provides some cli commands to
collect data and start online classification.

The other source is inside `arduino` directory.
It has c++ code for esp8266 compatible 
platforms to interact with the data recording  
web server from python.

### posture-detector http-logger
Starts a job for collecting data from a
web server and capturing keyboard so the
user can set the label for the current data
being recorded.

### posture-detector data-logger -baud 115200 -port /dev/ttyUSB0
This starts a similar job than the previous one 
but capturing data from serial bus.

### posture-detector run-api
Starts a uvicorn server that can receive 
unlabeled data, store it, and in another endpoint
provide the latest status as it was
classified by the model.

```
.
├── arduino
│   └── datalogger_analog_n_mcu
│       └── datalogger_analog_n_mcu
│           └── src
│               ├── main.cpp
│               └── MPUService.cpp
├── images
├── notebooks
│   ├── Angles - Extract and Visualize.ipynb
│   ├── LoadingAllDatasets.ipynb
│   ├── MainProcessing.ipynb
│   ├── new_test_12021_03_05.ipynb
│   ├── Regressor.ipynb
│   ├── Untitled.ipynb
│   ├── VaryingAngles.ipynb
│   └── Wearable - Extract and Visualize.ipynb
├── posture_detector
│   ├── api
│   │   ├── endpoints.py
│   │   ├── handlers.py
│   │   └── __init__.py
│   ├── commands
│   │   ├── commands.py
│   │   ├── http_logger.py
│   │   ├── __init__.py
│   │   └── serial_logger.py
│   ├── constants
│   │   ├── columns
│   │   │   ├── dataset.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── load_file.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── models
│   │   ├── classification.py
│   │   ├── __init__.py
│   │   ├── regressor.py
│   │   └── tasks.py
│   └── viz
│       ├── __init__.py
│       └── plots.py
├── README.md
├── requirements.txt
├── sensors.md
└── setup.py


```

## Hardware
