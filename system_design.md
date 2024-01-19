# System Design Document - STIM300 Simulator

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. System Overview](#2-system-overview)
- [3. Components](#3-components)
  - [3.1. STIM300 Simulator Script](#31-stim300-simulator-script)
  - [3.2. Serial Communication](#32-serial-communication)
  - [3.3. User Command Processing](#33-user-command-processing)
- [4. Data Simulation](#4-data-simulation)
  - [4.1. Datagram Simulation](#41-datagram-simulation)
  - [4.2. Command Processing](#42-command-processing)
- [5. Serial Communication](#5-serial-communication)
  - [5.1. Virtual Serial Port Setup](#51-virtual-serial-port-setup)
  - [5.2. Sending and Receiving Data](#52-sending-and-receiving-data)
- [6. Command Processing](#6-command-processing)
  - [6.1. User Commands](#61-user-commands)
  - [6.2. Switch Function](#62-switch-function)
- [7. Exception Handling](#7-exception-handling)
- [8. Conclusion](#8-conclusion)

## 1. Introduction
This document outlines the design of the STIM300 Simulator, a Python script that simulates data transmission for the STIM300 inertial measurement unit.

## 2. System Overview
The system consists of a Python script running on a computer, simulating data transmission through a virtual serial port which are connected on port 9 and 10 but feel free to change.

## 3. Components

### 3.1. STIM300 Simulator Script
- Responsible for simulating STIM300 data transmission.
- Uses the `serial` library for communication.
- Processes user commands and proceed the correct actions.

### 3.2. Serial Communication
- Manages the setup and communication with the virtual serial port.
- Handles sending and receiving data.

### 3.3. User Command Processing
- Processes user commands and initiates actions.
- Utilizes the `switch` function to determine the type of action to perform.

## 4. Data Simulation

### 4.1. Datagram Simulation
- Generates simulated datagrams based on predefined formats(Follows the STIM300 datasheet).
- Simulates various types of datagrams (part number, serial number, configuration, etc.).

### 4.2. Command Processing
- Processes user commands received over the serial port.
- Invokes functions to simulate and transmit relevant data.

## 5. Serial Communication

### 5.1. Virtual Serial Port Setup
- Establishes a connection with the virtual serial port.
- Handles potential exceptions during port setup.

### 5.2. Sending and Receiving Data
- Implements functions for sending and receiving data over the serial port.
- Checks for incoming commands from the receiver.

## 6. Command Processing

### 6.1. User Commands
- Defines supported user commands for initiating specific actions.
- Commands include 'N', 'I', 'C', 'T', 'E', 'R', 'SERVICEMODE'.

### 6.2. Switch Function
- Processes user commands and triggers relevant actions based on the command.

## 7. Exception Handling
- Handles potential exceptions during serial port setup and data transmission.
- Ensures proper termination of the script.

## 8. Conclusion
- Summarizes the key components and functionality of the STIM300 Simulator.
- Provides an overview of the simulated data and user command processing.