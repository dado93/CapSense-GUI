# Capacitance Data - Kivy GUI
This repository contains the code required to run a Kivy-based GUI for plotting data streamed from a PSoC device related to capacitance measurements (4-channels), temperature and humidity. The data are collected using the following sensors:
- [FDC1004Q]() by Texas Instruments
- [SHT85]() by Sensirion

Data are streamed using a [RN-42]() Bluetooth module. 

## Requirements
- Kivy >= 1.1
- PySerial
- Loguru

## GUI Features
- Automatic discovery of the correct serial port among those available on the machine
- Plotting of data with variable sample rates with automatic adjustaments of the plots
- Configurable plot settings
- Data export to CSV/txt format

## Documentation Creation
Documentation is generated using pdoc3 and pushed to GitHub pages at the following link: [https://dado93.github.io/CapSense-GUI/](https://dado93.github.io/CapSense-GUI/)

In order to create the updated documentation, simply run:

`make docs`

and the updated documentation will be available in the docs folder.